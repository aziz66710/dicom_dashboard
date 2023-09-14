import React, {useState, useEffect} from 'react'
import {Deploy} from './Component/Deploy/Deploy';
import { API } from 'aws-amplify';
// use state create state variable = store backend
// use effect 
function App() {
    useEffect(() => {
        const getData = async () => {
            const data = await API.get("flaskapi","/items")
            console.log(data)
        }
        getData()
    })
        
    // const [data, setData] = useState([{}])

    // useEffect(() => {    
    //     fetch("/members").then(
    //         res => res.json()
    //     ).then(
    //         data => {
    //             setData(data)
    //             console.log(data)
    //         }
    //     )
    // }, [] )

    return (
        <div>
            {/* <Deploy prop={data}></Deploy> */}

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
