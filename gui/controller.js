import Modal from "./modal.js"
import Router from "./router.js"
import Question from "./question.js"
import Server from "./server.js"

/**
 * Global setup for connection to backend
 */
const host = "localhost"
const port = 9999

const Controller = {}
/**
 * Cloze Exercise
 */
Controller.cloze = () => {
    const connection = Server(port, host)
    const question = Question.connect(connection)
    question.flush()

    const choiceBtns = Question.choiceElements();
    choiceBtns.forEach(choiceBtn => {
        choiceBtn.addEventListener("click", (event) => {

            //fill
            const letter = event.target.querySelector("b").innerHTML
            question.fill(letter)

            //evaluate
            const choice = event.target.innerHTML.replace(
                event.target.querySelector("b").outerHTML,
                "")
            question.evaluate(choice)
        })
    });

    const nextBtn = document.getElementById("operation-next")
    nextBtn.addEventListener("click", (event) => {
        question.flush()
    })

    const removeBtn = document.getElementById("operation-remove")
    removeBtn.addEventListener("click", (event) => {
        question.remove()
    })
}

/**
 * Editor
 */
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
Editor.save = async (connection, command, args = []) => {
    const editor = document.getElementById("editor-input")
    const savebtn = document.querySelector("div.editor-panel button.editor-submit")
    savebtn.addEventListener("click", async (event) => {
        let text = editor.value;
        args.push(text);
        let result = await connection.invoke(command, args)
        Modal.notice(result.info)
        Router.cloze()
    })
    return Editor
}
Editor.cancel = () => {
    const returnbtn = document.querySelector("div.editor-panel button.editor-return")
    returnbtn.addEventListener("click", (event) => {
        Router.cloze()
    })
    return Editor
}

/**
 * Source List 
 */
Controller.source = async () => {
    const connection = Server(port, host)
    Editor.init(connection, "get_source_list")
    Editor.save(connection, "save_source_list")
    Editor.cancel()
}

/**
 * Config file
 */
Controller.config = async () => {
    const connection = Server(port, host)
    Editor.init(connection, "get_config");
    Editor.save(connection, "save_config");
    Editor.cancel()
}

/**
 * Keywords 
 */
Controller.keywords = async () => {
    const connection = Server(port, host)
    Editor.init(connection, "get_keywords", [], ",")
    Editor.save(connection, "save_keywords")
    Editor.cancel()
}

/**
 * Wrong Log
 */
Controller.wronglog = async () => {
    const connection = Server(port, host)
    Editor.iterate(connection, 'get_wrong_log')
    Editor.cancel()
}

/**
 * Operation Buttons in the footer
 * Where Navigation happens
 */
Controller.operation = () => {
    const connection = Server(port, host)

    //Prompt to deliver command to backend
    const handle = (command, args = [], text, handler) => {
        //const text = "Do you want to fresh questions?"
        Modal.prompt(text, async () => {
            Modal.waitting().start()
            let data = await connection.invoke(command, args)
            data = data.line
            Modal.waitting().end().notice(data)
            handler()
        })
    }

    //setup database
    const setupBtn = document.getElementById("setup-btn")
    setupBtn.addEventListener("click", (event) => {
        const text = "Do you want to rebuild your database?"
        handle("setup", [], text, async () => {
            Modal.waitting().start()
            let data = await connection.invoke("fresh")
            data = data.line
            Modal.waitting().end().notice(data)
            Question.flush()
        })
    })

    //fresh questions 
    const freshBtn = document.getElementById("fresh-btn")
    freshBtn.addEventListener("click", (event) => {
        const text = "Do you want to fresh new questions?";
        handle("fresh", [], text, () => {
            Question.flush()
        })
    })

    //setup source list
    const sourceBtn = document.getElementById("source-btn")
    sourceBtn.addEventListener("click", (event) => {
        Router.source()
    })

    //config file
    const configBtn = document.getElementById("config-btn")
    configBtn.addEventListener("click", (event) => {
        Router.config()
    })

    //keywords
    const keywordBtn = document.getElementById("keyword-btn")
    keywordBtn.addEventListener("click", (event) => {
        Router.keywords()
    })

    //Wrong log
    const wrongLogBtn = document.getElementById("wrong-log-btn")
    wrongLogBtn.addEventListener("click", (event) => {
        Router.wronglog()
    })
}

export default Controller