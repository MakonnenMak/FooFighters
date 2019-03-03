import React, { Component } from 'react';
import Login from './loginPage';
import NewReceipt from './NewReceipt';
import './App.css';
import { Route, BrowserRouter as Router } from 'react-router-dom';

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Route exact path="/" component={Login}/>
          <Route path="/dashboard" component={NewReceipt}/>
        </div>
      </Router>
    );
  }
}

export default App;
