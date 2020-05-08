import Modal from "./modal.js"
import Router from "./router.js"
import Question from "./question.js"
import Server from "./server.js"

/**
 * Global setup for connection to backend
 */
const host = "localhost"
const port = 9998

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
 * Source List 
 */
Controller.source = () => {
    const connection = Server(port, host)

}

/**
 * Operation Buttons in the footer
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
}

export default Controller