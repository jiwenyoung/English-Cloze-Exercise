import Modal from "./modal.js"

const Question = {}

/**
 * Helper Functions
 */

const reconstructSentence = (sentence)=>{
    sentence = sentence.replace("_","|")
    sentence = sentence.split("|")
    let charCollection = []
    for (let char of sentence[1]){
        if( char !== '_'){
            charCollection.push(char)
        }
    }
    sentence[1] = charCollection.join("") 
    sentence = `${sentence[0]}<span></span>${sentence[1]}`;
    return sentence
}

const getDomOfQuestion = ()=>{
    const selectorPrefix = "section.work-space div.question div.content";
    const sentence = document.querySelector(`${selectorPrefix} p`)
    let choices = document.querySelector(`${selectorPrefix} ul`)
    choices = Array.from(choices.children)
    const evaulate = document.querySelector(`${selectorPrefix} div.evaulate`)
    const doms = {
        "sentence" : sentence,
        "choices" : choices,
        "evaulate" : evaulate
    }
    return doms
}

const writeDom = (doms,data)=>{
    doms["sentence"].innerHTML = data.sentence;
    let i = 0
    for (let choice of doms["choices"]){
        let pickableLetter = choice.children[0].outerHTML
        choice.innerHTML = `${pickableLetter}${data.choices[i]}`
        i = i + 1
    }
}

const formatEvaluateResult = (info,data) =>{
    info = info.split(" ")
    if(data.evaluate === true){
        info[0] = `<b class='correct'>${info[0]}</b> `
    }else{
        let choicesElements = getDomOfQuestion()['choices']
        let lastIndex = info.length - 1;
        let keyword = {
            "letter" : "",
            "word" : info[lastIndex]
        }
        choicesElements.forEach(element => {
            let letter = element.children[0].innerHTML
            let choice = element.innerHTML
            choice = choice.replace(`<b>${letter}</b>`,'')
            if(choice === keyword["word"]){
                keyword['letter'] = letter
            }
        });    
        info[0] = `<b class='wrong'>${info[0]}</b>`;
        info[lastIndex] = `<span>${keyword["letter"]}&nbsp;&nbsp;${keyword["word"]}</span>`;
    }
    info = info.join(" ")
    return info
}

const Options = {}
Options.disable = ()=>{
    Array.from(
        document.querySelector(".work-space .question ul").children
    ).forEach((element)=>{
        element.style.pointerEvents = "none"
    })
    return Options
}
Options.enable = ()=>{
    Array.from(
        document.querySelector(".work-space .question ul").children
    ).forEach((element)=>{
        element.style.pointerEvents = "auto"
    })
    return Options    
}
Options.highlight = (letter)=>{
    const elements = Question.choiceElements()
    elements.forEach((element)=>{
        if( element.querySelector('b').innerHTML === letter ){
            element.classList.add("selected")
        }
    })
    return Options
}
Options.unhighlight = ()=>{
    const elements = Question.choiceElements()
    elements.forEach((element)=>{
        if(element.classList.contains("selected")){
            element.classList.remove("selected")
        }
    })
    return Options
}  

const EvaluateInfo = {}
EvaluateInfo.getElement = ()=>{
    return document.querySelector(
        'section.work-space div.question div.evaulate'
    )
}
EvaluateInfo.open = (text)=>{
    const element = EvaluateInfo.getElement()
    element.innerHTML = text
    element.style.visibility = "visible"
    return EvaluateInfo
}
EvaluateInfo.close = ()=>{
    const element = EvaluateInfo.getElement()
    element.innerHTML = ""
    element.style.visibility = "hidden"
    return EvaluateInfo    
}

/**
 * Object Methods
 */

Question.connection = {}
Question.connect = (connection)=>{
    Question.connection = connection
    return Question
}

Question.flush = async ()=>{
    Options.unhighlight()
    EvaluateInfo.close()
    Question.total()
    const connection = Question.connection;
    const data = await connection.invoke("rollout")
    data.sentence = reconstructSentence(data.sentence)
    const doms = getDomOfQuestion()
    writeDom(doms,data)
    Options.enable()
    return Question
}

Question.evaluate = async (answer)=>{
    const connection = Question.connection;
    const data = await connection.invoke("evaulate", [answer]);
    
    //display result infomation
    let info = data.info;
    info = formatEvaluateResult(info,data)
    EvaluateInfo.open(info)

    //make options unclickable
    Options.disable()

    //change score
    document.getElementById("correct-score").innerHTML = data.score.correct
    document.getElementById("wrong-score").innerHTML = data.score.wrong

    return Question
}

Question.choiceElements = ()=>{
    const selectorPrefix = "section.work-space div.question div.content";
    let choicesBtns = document.querySelector(`${selectorPrefix} ul`).children
    choicesBtns = Array.from(choicesBtns)
    return choicesBtns
}

Question.fill = (letter)=>{
    // fill in to gap in sentence
    const selectorPrefix = "section.work-space div.question div.content";
    const element = document.querySelector(`${selectorPrefix} p span`)
    element.innerHTML = letter

    // highlight selected option
    Options.highlight(letter)

    return Question
}

Question.remove = async ()=>{
    const connection = Question.connection;
    const result = await connection.invoke("remove")
    if(result.done === true){
        Question.flush()
    }else{
        Modal.notice(result.error)
        Question.flush()
    }
}

Question.total = async ()=>{
    const connection = Question.connection;
    const result = await connection.invoke("total")
    if(result.done === true){
        const totlaElement = document.querySelector("#total b")
        totlaElement.innerHTML = result.total
    }else{
        Modal.notice(result.error)
    }
}

export default Question