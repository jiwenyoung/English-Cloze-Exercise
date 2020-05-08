const View = {}

/**
 * Cloze Test
 */
View.cloze = ()=>{
    const html  = `<div class="question">
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
        render : ()=>{
            View.render(html)
        }
    }
}
 
/**
 * Source List
 */
View.source = ()=>{
    const html = `<p>SOURCE LIST PLACE HOLDER</p>`
    return {
        render : ()=>{
            View.render(html)
        }
    }
}


View.render = (html)=>{
    const workSpace = document.querySelector("section.work-space")
    workSpace.innerHTML = ""
    workSpace.innerHTML = html 
}

export default View