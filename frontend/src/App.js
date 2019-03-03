import React, { Component } from 'react';
import Login from './loginPage';
import Homepage from './homepage';
import Select from './selectPage';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Select />
      </div>
    );
  }
}

export default App;
