const Question = {}

/**
 * Make the sentence suitable for GUI display
 */
const reconstructSentence = (sentence) => {
    sentence = sentence.replace("_", "|")
    sentence = sentence.split("|")
    let charCollection = []
    for (let char of sentence[1]) {
        if (char !== '_') {
            charCollection.push(char)
        }
    }
    sentence[1] = charCollection.join("")
    sentence = `${sentence[0]}<span></span>${sentence[1]}`;
    return sentence
}

/**
 * Get a set of dom nodes of cloze question
 */
const getDomOfQuestion = () => {
    const selectorPrefix = "section.work-space div.question div.content";
    const sentence = document.querySelector(`${selectorPrefix} p`)
    let choices = document.querySelector(`${selectorPrefix} ul`)
    choices = Array.from(choices.children)
    const evaulate = document.querySelector(`${selectorPrefix} div.evaulate`)
    const doms = {
        "sentence": sentence,
        "choices": choices,
        "evaulate": evaulate
    }
    return doms
}

/**
 * Write sentence and options into UI
 */
const writeDom = (doms, data) => {
    doms["sentence"].innerHTML = data.sentence;
    let i = 0
    for (let choice of doms["choices"]) {
        let pickableLetter = choice.children[0].outerHTML
        choice.innerHTML = `${pickableLetter}${data.choices[i]}`
        i = i + 1
    }
}

/**
 * Switch display/hidden of cloze question area
 */
const ClozeArea = {}
ClozeArea.display = () => {
    const container = document.querySelector("section.work-space .question")
    container.style.visibility = "visible"
}
ClozeArea.hide = ()=>{
    const container = document.querySelector("section.work-space .question")
    container.style.visibility = "hidden"    
}

/**
 * Switch display/hidden of operation buttons
 */
const OperationButtons = {}
OperationButtons.display = ()=>{
    const container = document.querySelector("div.operation")
    container.style.visibility = "visible"
}
OperationButtons.hide = ()=>{
    const container = document.querySelector("div.operation")
    container.style.visibility = "hidden"
}

/**
 * Switch no-more-question to display/hidden
 */
const NoMoreQuestionArea = {}
NoMoreQuestionArea.display = ()=>{
    const container = document.querySelector(".no-more-question")
    container.style.visibility = "visible"
}
NoMoreQuestionArea.hide = ()=>{
    const container = document.querySelector(".no-more-question")
    container.style.visibility = "hidden"
}

/**
 * format the display of evaluation result
 */
const formatEvaluateResult = (info, data) => {
    info = info.split(" ")
    if (data.evaluate === true) {
        info[0] = `<b class='correct'>${info[0]}</b> `
    } else {
        let choicesElements = getDomOfQuestion()['choices']
        let lastIndex = info.length - 1;
        let keyword = {
            "letter": "",
            "word": info[lastIndex]
        }
        choicesElements.forEach(element => {
            let letter = element.children[0].innerHTML
            let choice = element.innerHTML
            choice = choice.replace(`<b>${letter}</b>`, '')
            if (choice === keyword["word"]) {
                keyword['letter'] = letter
            }
        });
        info[0] = `<b class='wrong'>${info[0]}</b>`;
        info[lastIndex] = `<span>${keyword["letter"]}&nbsp;&nbsp;${keyword["word"]}</span>`;
    }
    info = info.join(" ")
    return info
}

/**
 * Options offer to be picked
 */
const Options = {}
Options.disable = () => {
    Array.from(
        document.querySelector(".work-space .question ul").children
    ).forEach((element) => {
        element.style.pointerEvents = "none"
    })
    return Options
}
Options.enable = () => {
    Array.from(
        document.querySelector(".work-space .question ul").children
    ).forEach((element) => {
        element.style.pointerEvents = "auto"
    })
    return Options
}
Options.highlight = (letter) => {
    const elements = Question.choiceElements()
    elements.forEach((element) => {
        if (element.querySelector('b').innerHTML === letter) {
            element.classList.add("selected")
        }
    })
    return Options
}
Options.unhighlight = () => {
    const elements = Question.choiceElements()
    elements.forEach((element) => {
        if (element.classList.contains("selected")) {
            element.classList.remove("selected")
        }
    })
    return Options
}

/**
 * The infomation of evaulation
 */
const EvaluateInfo = {}
EvaluateInfo.getElement = () => {
    return document.querySelector(
        'section.work-space div.question div.evaulate'
    )
}
EvaluateInfo.open = (text) => {
    const element = EvaluateInfo.getElement()
    element.innerHTML = text
    element.style.visibility = "visible"
    return EvaluateInfo
}
EvaluateInfo.close = () => {
    const element = EvaluateInfo.getElement()
    element.innerHTML = ""
    element.style.visibility = "hidden"
    return EvaluateInfo
}

/**
 * Status bottons
 */
const Status = {}
Status.update = (status)=>{
    if(status === 0){
        let statusBtn = document.getElementById("status-new")
        statusBtn.classList.add("status-selected")
        statusBtn = document.getElementById("status-wrong")
        if(statusBtn.classList.contains("status-selected")){
            statusBtn.classList.remove("status-selected")
        }
    }else{
        let statusBtn = document.getElementById("status-wrong")
        statusBtn.classList.add("status-selected")
        statusBtn = document.getElementById("status-new")
        if(statusBtn.classList.contains("status-selected")){
            statusBtn.classList.remove("status-selected")
        }
    }
}

/**
 * Next Button
 */
const NextButton = {}
NextButton.disable = ()=> {
    const button = document.getElementById("operation-next")
    button.classList.add("disable")
}
NextButton.able = ()=>{
    const button = document.getElementById("operation-next")
    button.classList.remove("disable")
}


/**
 * No More Quesiotn in DB
 */
const noMoreQuestion = (text)=>{
    ClozeArea.hide()
    OperationButtons.hide()
    const container = document.querySelector("p.no-more-question")
    container.innerHTML = text 
    NoMoreQuestionArea.display()
}

/**
 * Object Methods
 */
Question.connection = {}
Question.connect = (connection) => {
    Question.connection = connection
    return Question
}

Question.flush = async (status = 0) => {
    NoMoreQuestionArea.hide()
    Options.unhighlight()
    EvaluateInfo.close()
    NextButton.disable()
    Question.total(status)
    Status.update(status)
    const connection = Question.connection;
    const data = await connection.invoke("rollout", [status])
    if(data.done === true){
        data.sentence = reconstructSentence(data.sentence)
        const doms = getDomOfQuestion()
        writeDom(doms, data)
        OperationButtons.display()
        ClozeArea.display()
        Options.enable()
    }else{
        noMoreQuestion(data.info)
    }
    return Question
}

Question.evaluate = async (answer) => {
    const connection = Question.connection;
    const data = await connection.invoke("evaulate", [answer]);

    //display result infomation
    let info = data.info;
    info = formatEvaluateResult(info, data)
    EvaluateInfo.open(info)

    //make options unclickable
    Options.disable()

    //change score
    document.getElementById("correct-score").innerHTML = data.score.correct
    document.getElementById("wrong-score").innerHTML = data.score.wrong

    //enable next button
    NextButton.able()

    return Question
}

Question.choiceElements = () => {
    const selectorPrefix = "section.work-space div.question div.content";
    let choicesBtns = document.querySelector(`${selectorPrefix} ul`).children
    choicesBtns = Array.from(choicesBtns)
    return choicesBtns
}

Question.fill = (letter) => {
    // fill in to gap in sentence
    const selectorPrefix = "section.work-space div.question div.content";
    const element = document.querySelector(`${selectorPrefix} p span`)
    element.innerHTML = letter

    // highlight selected option
    Options.highlight(letter)

    return Question
}

Question.remove = async (done_handler=null,error_handler=null) => {
    const connection = Question.connection;
    const result = await connection.invoke("remove")
    if (result.done === true) {
        done_handler()
    } else {
        error_handler(result.error)
    }
}

Question.total = async ( status = 0 ) => {
    const connection = Question.connection;
    const result = await connection.invoke("total", [ status ])
    if (result.done === true) {
        const totalContainer = document.getElementById("total")        
        totalContainer.innerHTML = `Totally <b></b> cloze inside database`
        const totlaElement = document.querySelector("#total b")
        totlaElement.innerHTML = result.total
    } else {
        const totalContainer = document.getElementById("total")        
        totalContainer.innerHTML = result.error
    }
}

export default Question