import React, { Component } from 'react';
import Login from './loginPage';
import NewReceipt from './NewReceipt';
import Homepage from './homepage';
// import Select from './selectPage';
import './App.css';
import { Route, BrowserRouter as Router } from 'react-router-dom';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userEmail: "",
    }
  }

  render() {
    const login = () => <Login rootState={this.state} setRootState={this.setState.bind(this)}/>
    const homepage = () => <Homepage rootState={this.state} setRootState={this.setState.bind(this)}/>
    const newReceipt = () => <NewReceipt rootState={this.state} setRootState={this.setState.bind(this)}/>
    return (
      <Router>
        <div className="App">
          <Route exact path="/" component={login}/>
          <Route path="/dashboard" component={homepage}/>
          <Route path="/newreceipt" component={newReceipt}/>
        </div>
      </Router>
    );
  }
}

export default App;
