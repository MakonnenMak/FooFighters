import React, { Component } from 'react';
import Login from './loginPage';
import NewReceipt from './NewReceipt';
import Homepage from './homepage';
import Select from './selectPage';
import './App.css';
import { Route, BrowserRouter as Router } from 'react-router-dom';

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Route exact path="/" component={Login}/>
          <Route path="/dashboard" component={Homepage}/>
          <Route path="/newreceipt" component={NewReceipt}/>
          <Route path="/editreceipt" component={Select}/>
        </div>
      </Router>
    );
  }
}

export default App;