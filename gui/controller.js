const { shell } = require('electron')
const querystring = require("querystring")
const path = require("path")

import Modal from "./modal.js"
import Router from "./router.js"
import Question from "./question.js"
import Server from "./server.js"
import Editor from "./Editor.js"

/**
 * Global setup for connection to backend
 */
const Storage = {
    host: "localhost",
    port: 9999,
    cloze_status: 0
}
const ENV = querystring.parse(global.location.search)["?env"]

const Controller = {}
/**
 * Init
 */
Controller.init = async ()=>{
    const connection = Server(Storage.port, Storage.host)
    let result = await connection.invoke("is_tables_setup")
    if(result.setup == 1){
        const element = document.getElementById("setup-btn")
        element.click()
    }else if(result.setup == 2){
        Modal.notice(result.info)
    }
}

/**
 * Cloze Exercise
 */
Controller.cloze = (status = Storage.cloze_status) => {
    const connection = Server(Storage.port, Storage.host)
    const question = Question.connect(connection)
    question.flush(status)

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
        question.flush(Storage.cloze_status)
    })

    const removeBtn = document.getElementById("operation-remove")
    removeBtn.addEventListener("click", (event) => {
        question.remove(()=>{
            question.flush(Storage.cloze_status)
        },(error)=>{
            Modal.notice(error)
        })
    })

    const statusBtn = {
        "new" : document.getElementById("status-new"),
        "wrong" : document.getElementById("status-wrong")
    }
    statusBtn["new"].addEventListener("click",()=>{
        Storage.cloze_status = 0
        Question.flush(Storage.cloze_status)
    })
    statusBtn["wrong"].addEventListener("click",()=>{
        Storage.cloze_status = 1
        Question.flush(Storage.cloze_status)
    })
}

/**
 * Source List 
 */
Controller.source = async () => {
    const connection = Server(Storage.port, Storage.host)
    Editor.init(connection, "get_source_list")
    Editor.save(connection, "save_source_list", [], (info) => {
        Modal.notice(info)
        Router.cloze()
    })
    Editor.cancel(() => {
        Router.cloze()
    })
}

/**
 * Open the souce file folder
 */
Controller.file = ()=>{
    let articleFolder = '';
    if(ENV === 'development'){
        articleFolder = path.join(__dirname,"..","cli","articles","*")
    }else if(ENV === 'production'){
        articleFolder = path.join(__dirname,"..","cloze","articles","*")
    }
    shell.showItemInFolder(articleFolder)
}

/**
 * Config file
 */
Controller.config = async () => {
    const connection = Server(Storage.port, Storage.host)
    Editor.init(connection, "get_config");
    Editor.save(connection, "save_config", [], (info) => {
        Modal.notice(info)
        Router.cloze()
    });
    Editor.cancel(() => {
        Router.cloze()
    })
}

/**
 * Keywords 
 */
Controller.keywords = async () => {
    const connection = Server(Storage.port, Storage.host)
    Editor.init(connection, "get_keywords", [], ",")
    Editor.save(connection, "save_keywords", [], (info) => {
        Modal.notice(info)
        Router.cloze()
    })
    Editor.cancel(() => {
        Router.cloze()
    })
}

/**
 * Wrong Log
 */
Controller.wronglog = async () => {
    const connection = Server(Storage.port, Storage.host)
    Editor.iterate(connection, 'get_wrong_log')
    Editor.cancel(() => {
        Router.cloze()
    })
}

/**
 * Operation Buttons in the footer
 * Where Navigation happens
 */
Controller.operation = () => {
    const connection = Server(Storage.port, Storage.host)

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
            Question.flush(Storage.cloze_status)
        })
    })

    //fresh questions 
    const freshBtn = document.getElementById("fresh-btn")
    freshBtn.addEventListener("click", (event) => {
        const text = "Do you want to fresh new questions?";
        handle("fresh", [], text, () => {
            Question.flush(Storage.cloze_status)
        })
    })

    //setup url source list
    const sourceBtn = document.getElementById("source-btn")
    sourceBtn.addEventListener("click", (event) => {
        Router.source()
    })

    //setup file source folder
    const fileBtn = document.getElementById("file-btn")
    fileBtn.addEventListener("click",(event)=>{
        Router.file()
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