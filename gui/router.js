import Controller from "./controller.js"
import View from "./view.js"

const Router = {}
Router.cloze = ()=>{
    View.cloze().render()
    Controller.cloze()
}

Router.source = ()=>{
    View.source().render()
    Controller.source()
}

Router.operation = ()=>{
    Controller.operation()
} 

export default Router