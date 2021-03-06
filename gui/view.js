const View = {}

/**
 * Cloze Test
 */
View.cloze = () => {
    const html = `<div class="status-buttons">
                      <span class="new-cloze" id="status-new">
                          new cloze
                      </span>
                      <span class="wrong-cloze" id="status-wrong">
                          wrong cloze
                      </span>
                  </div>
                  <div class="question">
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
                   </div>
                   <p class='no-more-question'>
                        No More Cloze Question
                   </p>`
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

View.render = (html) => {
    const workSpace = document.querySelector("section.work-space")
    workSpace.innerHTML = ""
    workSpace.innerHTML = html
}

export default View