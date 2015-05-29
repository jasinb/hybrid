import {Socket} from "phoenix"

let agentContainer = $("#agents")
let socket = new Socket("/ws")
socket.connect()
let chan = socket.chan("agents:", {})
chan.join().receive("ok", chan => {
    console.log("Joined channel!")
})

chan.on("agent_update", payload => {
    console.log(payload.agent + ' ' + payload.state)
    var item = '<div id="' + payload.agent + '">'
    item += payload.agent + ': ' + payload.state
        item += '<div class="progress progress-striped">'
    if (payload.state === 'idle')
        item += '<div class="progress-bar progress-bar-success" '
    else
        item += '<div class="progress-bar progress-bar-info" '
    if (payload.state === 'computing')
    {
        item += 'style="min-width: 20px; width: ' + Math.round(payload.progress * 100.0) + '%;">'
        item += Math.round(100.0 * payload.progress) + '%'
    }
    else
    {
        item += 'style="width: 100%;">'
        item += payload.state
    }
    item += '</div></div>'
    item += '</div>'
    var el = agentContainer.find("#" + payload.agent)
    if (!el.length)
    {
        agentContainer.append(item)
    }
    else
    {
        el.replaceWith(item)
    }
})

let App = {
}

export default App
