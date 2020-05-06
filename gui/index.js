import server from "./server.js"

const run = async ()=>{
    let connection = server(9998,"localhost")
    const data = await connection.invoke("rollout")

    let container = document.getElementById("container")
    container.innerHTML = `<p>${data.sentence}</p><p>${data.choices}</p><p>${data.keyword}</p>`
    console.log(data)

    let button = document.getElementById("answer")
    button.addEventListener('click',async (event)=>{
        let connection = server(9998,"localhost")
        const result = await connection.invoke("evaulate",['over'])
        console.log(result)
    })
}

run()




