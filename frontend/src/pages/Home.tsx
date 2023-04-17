import './Home.css'

import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const INITIAL_STATE = [
  { id: 1, book_Title: 'Tommy', age: 21, hobby: 'coding' },
  { id: 2, name: 'Anna', age: 19, hobby: 'reading' },
  { id: 3, name: 'Bobby', age: 16, hobby: 'swimming' },
  { id: 4, name: 'Lauren', age: 25, hobby: 'running' },
]

const capitalize = (word: string) => {
  return (word[0].toUpperCase() + word.slice(1)).replaceAll('_', ' ')
}

export const Home = () => {
  const [users, setUsers] = useState(INITIAL_STATE)

  const loginLink = (
    <Link to="/">
      <button className="logout">Log out</button>
    </Link>
  )

  const renderUsers = () => {
    return INITIAL_STATE.map(({ id, name, age, hobby }) => {
      return (
        <tr key={id}>
          <td>{id}</td>
          <td>{name}</td>
          <td>{age}</td>
          <td>{hobby}</td>
          <td>
            <button>Buy</button>
          </td>
        </tr>
      )
    })
  }

  const renderHeader = () => {
    return (
      <tr>
        {Object.keys(INITIAL_STATE[0]).map((key) => (
          <th>{capitalize(key)}</th>
        ))}
      </tr>
    )
  }

  const renderTable = () => {
    return (
      <table>
        {renderHeader()}
        <tbody>{renderUsers()}</tbody>
      </table>
    )
  }

  return (
    <div className="home">
      <h1>Textbook Exchange System</h1>

      {loginLink}

      <div className="book-list">
        <h2>Available Books</h2>
        {renderTable()}
      </div>
      <div className="account-info">
        <h2>Account Information</h2>
        <p>Account ID: </p>
        <p>Token Number: </p>
        <p>List of Purchased Books:</p>
        <ul></ul>
        <p>List of Contributed Books:</p>
        <ul></ul>

        <button className="make_contribute">Make a Contribution</button>
      </div>
    </div>
  )
}

export default Home
