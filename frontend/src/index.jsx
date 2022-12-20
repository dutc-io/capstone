import { createRoot } from 'react-dom/client'
import { get } from 'superagent'
import { useState, useEffect } from 'react'

const Counter = () => {
    const [ ready, setReady ] = useState(false)
    const [ count, setCount ] = useState({local: null, remote: null})
    useEffect(() => {
        const ws = new WebSocket(`ws://${document.location.host}/wsapi/ws`)
        ws.onopen = event => {
            setReady(true)
        }
        ws.onmessage = event => {
            const { data: rawData } = event
            const { count } = JSON.parse(rawData)
            console.log({ count })
            // setCount(({ local }) => ({local: local + 1, remote: count}))
        }
    }, [])

    if (!ready) return <em>Still loading...</em>
    return <>Count: <b>{ count.local }</b> v <b>{ count.remote }</b> (diff: {count.remote - count.local})</>
}

const Layout = () => <>
    <h1>Cassino</h1>
    <Counter />
    <p>Instructions for play.</p>
    Players:
    <br />
    Deck:
    <br />
    Table:
    <br />
    Hand:
</>

const App = () => <>
    <Layout />
</>

createRoot(
    document.getElementById('root')
).render(<App />)

