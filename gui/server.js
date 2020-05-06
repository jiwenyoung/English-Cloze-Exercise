const net = require('net');

const server = (port, address) => {
    const connection = net.connect(port, address)
    return {
        invoke: async (name, args = [], handler=null) => {
            let data = {
                name: name,
                arguments: args
            }
            data = JSON.stringify(data)
            connection.write(data)

            let response = ""
            let errors = []
            await (() => {
                const promise = new Promise((resolve, reject) => {
                    connection.on("data", (data) => {
                        if(handler !== null){
                            data = JSON.parse(data.toString("utf-8"))
                            handler(data)                            
                        }
                        response = response + data
                        resolve(response)
                    })
                    connection.on("error", (error) => {
                        errors.push(error)
                        reject(error)
                    })
                })
                return promise
            })()

            if (errors.length > 0) {
                return false
            } else {
                if(handler === null){
                    response = JSON.parse(response.toString("utf-8"))
                    return response
                }else{
                    return true
                }
            }
        },
        connect: () => {
            return connection
        }
    }
}

export default server