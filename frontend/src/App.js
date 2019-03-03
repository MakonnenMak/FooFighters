import React, { Component } from 'react';
import Login from './loginPage';
import Homepage from './homepage';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Login />
        <Homepage />
      </div>
    );
  }
}

export default App;
