(function () {
    var subjectBody = document.querySelector('[data-subject-body]');
    var conflictList = document.querySelector('[data-conflict-list]');
    var fromSelect = document.getElementById('conflictFrom');
    var toSelect = document.getElementById('conflictTo');
    var addSubjectButton = document.getElementById('addSubjectBtn');
    var addConflictButton = document.getElementById('addConflictBtn');
    var newSubjectName = document.getElementById('newSubjectName');
    var newSubjectTeacher = document.getElementById('newSubjectTeacher');
    var form = document.getElementById('coloringForm');
    var formAction = document.getElementById('formAction');
    var graphContainer = document.getElementById('graph-canvas');
    var fitGraphButton = document.getElementById('fitGraphBtn');
    var stabilizeGraphButton = document.getElementById('stabilizeGraphBtn');
    var subjectCountLabel = document.querySelector('[data-subject-count]');
    var conflictCountLabel = document.querySelector('[data-conflict-count]');
    var graphNetwork = null;

    var shiftColors = [
        '#c94d57',
        '#3a9d66',
        '#2e86ab',
        '#c28f2c',
        '#6f5aa8',
        '#2f8f83',
        '#d46a4c',
        '#4a6fa5'
    ];

    if (!subjectBody || !conflictList || !fromSelect || !toSelect || !form || !formAction) {
        return;
    }

    function escapeHtml(value) {
        return String(value || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function getSubjectItems() {
        var rows = subjectBody.querySelectorAll('tr');
        var subjects = [];
        var used = {};

        rows.forEach(function (row) {
            var nameInput = row.querySelector('.subject-name');
            var teacherInput = row.querySelector('input[name="teacher[]"]');
            var name = nameInput ? nameInput.value.trim() : '';
            var teacher = teacherInput ? teacherInput.value.trim() : '';
            var color = parseInt(row.getAttribute('data-color'), 10);

            if (!name || used[name]) {
                return;
            }

            used[name] = true;
            subjects.push({
                name: name,
                teacher: teacher,
                color: isNaN(color) ? 0 : color
            });
        });

        return subjects;
    }

    function getSubjects() {
        return getSubjectItems().map(function (subject) {
            return subject.name;
        });
    }

    function getConflicts() {
        var conflicts = [];
        conflictList.querySelectorAll('.conflict-item').forEach(function (item) {
            conflicts.push({
                from: item.getAttribute('data-conflict-from'),
                to: item.getAttribute('data-conflict-to')
            });
        });
        return conflicts;
    }

    function refreshRowNumbers() {
        subjectBody.querySelectorAll('tr').forEach(function (row, index) {
            var cell = row.querySelector('[data-row-number]');
            if (cell) {
                cell.textContent = index + 1;
            }
        });
    }

    function refreshConflictOptions() {
        var subjects = getSubjects();
        var oldFrom = fromSelect.value;
        var oldTo = toSelect.value;
        var options = subjects.map(function (name) {
            return '<option value="' + escapeHtml(name) + '">' + escapeHtml(name) + '</option>';
        }).join('');

        fromSelect.innerHTML = options;
        toSelect.innerHTML = options;

        if (subjects.indexOf(oldFrom) !== -1) {
            fromSelect.value = oldFrom;
        }
        if (subjects.indexOf(oldTo) !== -1) {
            toSelect.value = oldTo;
        } else if (subjects.length > 1) {
            toSelect.selectedIndex = 1;
        }
    }

    function refreshConflicts() {
        var subjects = getSubjects();
        var allowed = {};
        subjects.forEach(function (name) {
            allowed[name] = true;
        });

        conflictList.querySelectorAll('.conflict-item').forEach(function (item) {
            var left = item.getAttribute('data-conflict-from');
            var right = item.getAttribute('data-conflict-to');
            if (!allowed[left] || !allowed[right] || left === right) {
                item.remove();
            }
        });
    }

    function refreshEditor() {
        refreshRowNumbers();
        refreshConflictOptions();
        refreshConflicts();
        refreshCounts();
        drawGraph();
    }

    function refreshCounts() {
        if (subjectCountLabel) {
            subjectCountLabel.textContent = getSubjectItems().length;
        }
        if (conflictCountLabel) {
            conflictCountLabel.textContent = getConflicts().length;
        }
    }

    function addSubject(name, teacher) {
        var row = document.createElement('tr');
        row.innerHTML = [
            '<td data-row-number></td>',
            '<td><input type="text" name="subject[]" class="form-control subject-name" value="' + escapeHtml(name) + '"></td>',
            '<td><input type="text" name="teacher[]" class="form-control" value="' + escapeHtml(teacher) + '"></td>',
            '<td><button type="button" class="table-action" data-remove-subject aria-label="Удалить дисциплину">×</button></td>'
        ].join('');
        subjectBody.appendChild(row);
        refreshEditor();
    }

    function conflictExists(left, right) {
        var exists = false;
        conflictList.querySelectorAll('.conflict-item').forEach(function (item) {
            var itemLeft = item.getAttribute('data-conflict-from');
            var itemRight = item.getAttribute('data-conflict-to');
            if ((itemLeft === left && itemRight === right) || (itemLeft === right && itemRight === left)) {
                exists = true;
            }
        });
        return exists;
    }

    function addConflict(left, right) {
        if (!left || !right || left === right || conflictExists(left, right)) {
            return;
        }

        var item = document.createElement('div');
        item.className = 'conflict-item';
        item.setAttribute('data-conflict-from', left);
        item.setAttribute('data-conflict-to', right);
        item.innerHTML = [
            '<span>' + escapeHtml(left) + ' - ' + escapeHtml(right) + '</span>',
            '<input type="hidden" name="conflict_from[]" value="' + escapeHtml(left) + '">',
            '<input type="hidden" name="conflict_to[]" value="' + escapeHtml(right) + '">',
            '<button type="button" class="table-action" data-remove-conflict aria-label="Удалить конфликт">×</button>'
        ].join('');
        conflictList.appendChild(item);
        refreshCounts();
        drawGraph();
    }

    function colorByShift(shift) {
        if (!shift) {
            return {
                background: '#ffffff',
                border: '#2e86ab',
                highlight: { background: '#e8eef5', border: '#1d3557' }
            };
        }

        var color = shiftColors[(shift - 1) % shiftColors.length];
        return {
            background: color,
            border: '#ffffff',
            highlight: { background: color, border: '#1d3557' }
        };
    }

    function graphLabel(text) {
        var words = String(text || '').trim().split(/\s+/);
        var lines = [];
        var line = '';

        words.forEach(function (word) {
            if ((line + ' ' + word).trim().length > 16 && line) {
                lines.push(line);
                line = word;
            } else {
                line = (line + ' ' + word).trim();
            }
        });

        if (line) {
            lines.push(line);
        }

        return lines.join('\n');
    }

    function fontColor(shift) {
        if (shift === 2 || shift === 3 || shift === 5 || shift === 6 || shift === 7 || shift === 8) {
            return '#ffffff';
        }
        return shift ? '#1d3557' : '#1d3557';
    }

    function drawGraph() {
        if (!graphContainer) {
            return;
        }

        if (typeof vis === 'undefined') {
            graphContainer.innerHTML = '';
            return;
        }

        var subjects = getSubjectItems();
        var subjectNames = {};
        var nodes = [];
        var edges = [];
        var usedEdges = {};
        var nodeView = graphNodeView(subjects.length);

        subjects.forEach(function (subject) {
            subjectNames[subject.name] = true;
            nodes.push({
                id: subject.name,
                label: graphLabel(subject.name),
                title: subject.teacher ? subject.teacher : subject.name,
                shape: 'box',
                margin: nodeView.margin,
                widthConstraint: { minimum: nodeView.minWidth, maximum: nodeView.maxWidth },
                borderWidth: subject.color ? 3 : 2,
                color: colorByShift(subject.color),
                font: {
                    color: fontColor(subject.color),
                    size: nodeView.fontSize,
                    face: 'Arial',
                    bold: { color: fontColor(subject.color), size: nodeView.fontSize, face: 'Arial' },
                    strokeWidth: subject.color ? 0 : 3,
                    strokeColor: '#ffffff',
                    vadjust: 0
                },
                shadow: true
            });
        });

        getConflicts().forEach(function (conflict) {
            if (!subjectNames[conflict.from] || !subjectNames[conflict.to] || conflict.from === conflict.to) {
                return;
            }

            var key = [conflict.from, conflict.to].sort().join('::');
            if (usedEdges[key]) {
                return;
            }

            usedEdges[key] = true;
            edges.push({
                id: key,
                from: conflict.from,
                to: conflict.to,
                color: { color: '#8fa1b4', highlight: '#c94d57' },
                width: 2,
                selectionWidth: 4,
                smooth: { type: 'dynamic', roundness: 0.25 }
            });
        });

        var data = {
            nodes: new vis.DataSet(nodes),
            edges: new vis.DataSet(edges)
        };
        var options = {
            autoResize: true,
            layout: {
                improvedLayout: true,
                randomSeed: 7
            },
            interaction: {
                dragNodes: true,
                dragView: true,
                hover: true,
                multiselect: true,
                tooltipDelay: 80,
                zoomView: true
            },
            physics: {
                enabled: true,
                solver: 'repulsion',
                stabilization: { iterations: 220, updateInterval: 20 },
                repulsion: {
                    nodeDistance: nodeView.distance,
                    centralGravity: 0.16,
                    springLength: nodeView.spring,
                    springConstant: 0.09,
                    damping: 0.12
                }
            },
            nodes: {
                chosen: true
            },
            edges: {
                chosen: true
            }
        };

        if (graphNetwork) {
            graphNetwork.setOptions(options);
            graphNetwork.setData(data);
        } else {
            graphNetwork = new vis.Network(graphContainer, data, options);
        }

        resizeGraphCanvas();

        graphNetwork.once('stabilizationIterationsDone', function () {
            focusGraph(nodes.length);
        });

        window.setTimeout(function () {
            focusGraph(nodes.length);
        }, 1300);
    }

    function focusGraph(nodeCount) {
        if (!graphNetwork || !nodeCount) {
            return;
        }

        resizeGraphCanvas();

        var view = graphView(nodeCount);

        graphNetwork.stopSimulation();
        graphNetwork.moveTo({
            position: view.position,
            scale: view.scale,
            animation: { duration: 350, easingFunction: 'easeInOutQuad' }
        });
    }

    function resizeGraphCanvas() {
        var height = Math.max(graphContainer.clientHeight || 0, graphContainer.offsetHeight || 0, 560);
        var width = Math.max(graphContainer.clientWidth || 0, graphContainer.offsetWidth || 0, 900);
        var canvas = graphContainer.querySelector('canvas');

        graphContainer.style.height = height + 'px';
        graphNetwork.setSize('100%', height + 'px');

        if (canvas) {
            canvas.width = width;
            canvas.height = height;
            canvas.style.width = '100%';
            canvas.style.height = height + 'px';
        }

        graphNetwork.redraw();
    }

    function graphView(nodeCount) {
        var scale = graphScale(nodeCount);
        var position = graphCenter();

        try {
            graphNetwork.fit({ animation: false });
            position = graphNetwork.getViewPosition();
            scale = Math.min(scale, graphNetwork.getScale() * 2.1);
        } catch (error) {
            position = graphCenter();
        }

        return {
            position: position,
            scale: scale
        };
    }

    function graphScale(nodeCount) {
        if (nodeCount <= 5) {
            return 0.54;
        }
        if (nodeCount <= 10) {
            return 0.5;
        }
        if (nodeCount <= 16) {
            return 0.44;
        }
        return 0.36;
    }

    function graphCenter() {
        var positions = graphNetwork.getPositions();
        var keys = Object.keys(positions);

        if (!keys.length) {
            return { x: 0, y: 0 };
        }

        var minX = positions[keys[0]].x;
        var maxX = positions[keys[0]].x;
        var minY = positions[keys[0]].y;
        var maxY = positions[keys[0]].y;

        keys.forEach(function (key) {
            minX = Math.min(minX, positions[key].x);
            maxX = Math.max(maxX, positions[key].x);
            minY = Math.min(minY, positions[key].y);
            maxY = Math.max(maxY, positions[key].y);
        });

        return {
            x: (minX + maxX) / 2,
            y: (minY + maxY) / 2
        };
    }

    function graphNodeView(nodeCount) {
        if (nodeCount <= 5) {
            return {
                fontSize: 28,
                minWidth: 240,
                maxWidth: 380,
                margin: { top: 20, right: 26, bottom: 20, left: 26 },
                distance: 360,
                spring: 250
            };
        }
        if (nodeCount <= 10) {
            return {
                fontSize: 23,
                minWidth: 190,
                maxWidth: 320,
                margin: { top: 16, right: 22, bottom: 16, left: 22 },
                distance: 290,
                spring: 210
            };
        }
        if (nodeCount <= 16) {
            return {
                fontSize: 20,
                minWidth: 160,
                maxWidth: 280,
                margin: { top: 14, right: 18, bottom: 14, left: 18 },
                distance: 230,
                spring: 170
            };
        }
        return {
            fontSize: 18,
            minWidth: 140,
            maxWidth: 250,
            margin: { top: 12, right: 16, bottom: 12, left: 16 },
            distance: 200,
            spring: 150
        };
    }

    if (fitGraphButton) {
        fitGraphButton.addEventListener('click', function () {
            if (graphNetwork) {
                var view = graphView(getSubjectItems().length);
                graphNetwork.moveTo({
                    position: view.position,
                    scale: view.scale,
                    animation: { duration: 300, easingFunction: 'easeInOutQuad' }
                });
            }
        });
    }

    window.addEventListener('resize', function () {
        if (graphNetwork) {
            focusGraph(getSubjectItems().length);
        }
    });

    if (stabilizeGraphButton) {
        stabilizeGraphButton.addEventListener('click', function () {
            if (graphNetwork) {
                graphNetwork.setOptions({ physics: { enabled: true } });
                graphNetwork.stabilize(180);
                window.setTimeout(function () {
                    focusGraph(getSubjectItems().length);
                }, 300);
            }
        });
    }

    addSubjectButton.addEventListener('click', function () {
        var name = newSubjectName.value.trim();
        var teacher = newSubjectTeacher.value.trim();
        if (!name) {
            newSubjectName.focus();
            return;
        }
        if (!teacher) {
            newSubjectTeacher.focus();
            return;
        }
        addSubject(name, teacher);
        newSubjectName.value = '';
        newSubjectTeacher.value = '';
        newSubjectName.focus();
    });

    addConflictButton.addEventListener('click', function () {
        addConflict(fromSelect.value, toSelect.value);
    });

    subjectBody.addEventListener('click', function (event) {
        if (event.target.matches('[data-remove-subject]')) {
            event.target.closest('tr').remove();
            refreshEditor();
        }
    });

    subjectBody.addEventListener('input', function (event) {
        var row = event.target.closest('tr');
        if (row) {
            row.setAttribute('data-color', '');
        }
        if (event.target.matches('.subject-name')) {
            refreshEditor();
        } else {
            drawGraph();
        }
    });

    conflictList.addEventListener('click', function (event) {
        if (event.target.matches('[data-remove-conflict]')) {
            event.target.closest('.conflict-item').remove();
            refreshCounts();
            drawGraph();
        }
    });

    newSubjectName.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            addSubjectButton.click();
        }
    });

    newSubjectTeacher.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            addSubjectButton.click();
        }
    });

    document.querySelectorAll('[data-submit-action]').forEach(function (button) {
        button.addEventListener('click', function () {
            formAction.value = button.getAttribute('data-submit-action');
            form.submit();
        });
    });

    form.addEventListener('submit', function () {
        if (!formAction.value) {
            formAction.value = 'calculate';
        }
    });

    refreshEditor();
})();
