ace.edit(element, {
    mode: "ace/mode/javascript",
    selectionStyle: "text"
})
editor.setOptions({
    autoScrollEditorIntoView: true,
    copyWithEmptySelection: true,
});

editor.setOption("mergeUndoDeltas", "always");
