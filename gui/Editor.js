const Editor = {}
Editor.init = async (connection, command, args = [], seperator = "\n") => {
    const editor = document.getElementById("editor-input")
    const data = await connection.invoke(command, args)
    editor.value = ""
    for (let line of data) {
        editor.value = editor.value + line.trim() + seperator
    }
    return Editor
}
Editor.iterate = async (connection, command, args = []) => {
    const editor = document.getElementById("editor-input")
    editor.value = ''
    await connection.invoke(command, args, (data) => {
        editor.value = editor.value + data.line
    })
    return Editor
}
Editor.save = async (connection, command, args = [], handler=null) => {
    const editor = document.getElementById("editor-input")
    const savebtn = document.querySelector("div.editor-panel button.editor-submit")
    savebtn.addEventListener("click", async (event) => {
        let text = editor.value;
        args.push(text);
        let result = await connection.invoke(command, args)
        handler(result.info)
    })
    return Editor
}
Editor.cancel = (handler=null) => {
    const returnbtn = document.querySelector("div.editor-panel button.editor-return")
    returnbtn.addEventListener("click", (event) => {
        handler()
    })
    return Editor
}

export default Editor