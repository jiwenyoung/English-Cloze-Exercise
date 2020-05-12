import Controller from "./controller.js"
import View from "./view.js"

const Router = {}
Router.init = ()=>{
    Controller.init()
}

Router.cloze = ()=>{
    View.cloze().render()
    Controller.cloze()
}

Router.source = ()=>{
    View.editor("Source List").render()
    Controller.source()
}

Router.file = ()=>{
    Controller.file()
}

Router.config = ()=>{
    View.editor("Configuration File").render()
    Controller.config()
}

Router.keywords = ()=>{
    View.editor("Key Words").render()
    Controller.keywords()
}

Router.wronglog = ()=>{
    View.editor("Log For Wrong", false).render()
    Controller.wronglog()
}

Router.operation = ()=>{
    Controller.operation()
} 

export default Router