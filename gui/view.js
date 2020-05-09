const View = {}

/**
 * Cloze Test
 */
View.cloze = () => {
    const html = `<div class="question">
                        <div class="content">
                            <p></p>
                            <ul>
                                <li><b>A</b></li>
                                <li><b>B</b></li>
                                <li><b>C</b></li>
                                <li><b>D</b></li>
                            </ul>
                            <div class="evaulate"></div>
                        </div>
                   </div>
                   <div class="operation">
                        <span id="operation-remove">REMOVE</span>
                        <span id="operation-next">NEXT</span>
                   </div>`
    return {
        render: () => {
            View.render(html)
        }
    }
}

/**
 * Editor
 */
View.editor = (title, save = true) => {
    let html = "";
    if(save === true){
        html = `<div class="editor-panel">
                    <h2>${title}</h2>
                    <textarea class="editor-input" id="editor-input">
                    </textarea>
                    <div class="editor-buttons">
                        <button class="editor-return">Go back</button>
                        <button class="editor-submit">Save</button>
                    </div>
                </div>`
    }else{
        html = `<div class="editor-panel">
                    <h2>${title}</h2>
                    <textarea class="editor-input" id="editor-input" disabled>
                    </textarea>
                    <div class="editor-buttons">
                        <button class="editor-return">Go back</button>
                    </div>
                </div>`
    }
    return {
        render: () => {
            View.render(html)
        }
    }
}

/**
 * Wrong Log File
 */
View.wrongLog = () => {
    const html = ``;
    return {

    }
}

View.render = (html) => {
    const workSpace = document.querySelector("section.work-space")
    workSpace.innerHTML = ""
    workSpace.innerHTML = html
}

export default View