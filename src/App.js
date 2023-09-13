import React, {useState, useEffect} from 'react'
import {Deploy} from './Component/Deploy/Deploy';
// use state create state variable = store backend
// use effect 
function App() {

    const [data, setData] = useState([{}])

    useEffect(() => {
        fetch("/members").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [] )

    return (
        <div className='App'>
            <Deploy prop={data}></Deploy>

        </div>

        // <div>

        //     {(typeof data.members == 'undefined') ? (
        //         <p>Loading...</p>
        //     ) : (
        //         data.members.map((member,i) => (
        //             <p key={i}>{member}</p>
        //         ))
        //     )}

        // </div>
    );
}

export default App
