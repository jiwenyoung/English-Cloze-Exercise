const Modal = {}

Modal.flush = (container) => {
    const element = document.getElementById(container)
    element.innerHTML = ""
}

Modal.getRootOfModal = (container, id, view) => {
    let element = document.getElementById(container)
    element.innerHTML = view
    element = element.querySelector(`section#${id}`)
    return element
}

Modal.bindHandelr = (element, id, event, handler) => {
    let button = element.querySelector(`button#${id}`)
    button.addEventListener(event, handler)
}

Modal.removeHandler = (element, id, event, handler) => {
    let button = element.querySelector(`button#${id}`)
    button.removeEventListener(event, handler)
}

Modal.prompt = (text, handler) => {
    const view = `<section class="modal" id="prompt">
                    <div class="dialog">
                        <p>${text}</p>
                        <div class="yes-or-no">
                            <button id="select-confirm">Confirm</button>
                            <button id="select-cancel">Cancel</button>
                        </div>
                    </div>
                </section>`
    const element = Modal.getRootOfModal("modal-box", "prompt", view)
    element.style.visibility = "visible";
    const clear = ()=>{
        Modal.removeHandler(element, "select-confirm", "click", confirmHandler);
        Modal.removeHandler(element, "select-cancel", "click", cancelHandler);
        element.style.visibility = "hidden";
        Modal.flush('modal-box')        
    }
    const confirmHandler = ()=>{
        clear()
        handler()
    }
    const cancelHandler = () => {
        clear()
    }
    Modal.bindHandelr(element, "select-confirm", "click", confirmHandler);
    Modal.bindHandelr(element, "select-cancel", "click", cancelHandler);
    return Modal
}

Modal.waitting = () => {
    const view = `<section class="modal" id="waitting">
                      <div class="dialog">
                          <i class="fas fa-paper-plane"></i>
                          <p>Waiting...</p>
                      </div>
                  </section>`
    const element = Modal.getRootOfModal("modal-box", "waitting", view)
    return {
        start() {
            element.style.visibility = "visiable";
            return Modal
        },
        end() {
            element.style.visibility = "hidden";
            Modal.flush('modal-box')
            return Modal
        }
    }
}

Modal.notice = (text) => {
    const view = `<section class="modal" id="notice">
                        <div class="dialog">
                            <p>${text}</p>
                            <div class="yes-or-no">
                                <button id="select-confirm">Confirm</button>
                            </div>
                        </div>
                  </section>`
    const element = Modal.getRootOfModal('modal-box', 'notice', view)
    element.style.visibility = "visiable";
    const handler = () => {
        element.style.visibility = "hidden";
        Modal.removeHandler(element, "select-confirm", "click", handler)
        Modal.flush('modal-box')
    }
    Modal.bindHandelr(element, "select-confirm", "click", handler)
    return Modal
}

export default Modal