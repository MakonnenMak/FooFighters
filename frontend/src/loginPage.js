import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import { Link } from 'react-router-dom';

class Login extends Component {
  handleClick = () => {
    console.log(this.state.tfValue);
    this.props.setRootState({
      userEmail: this.state.tfValue
    });
  }

  handleTextFieldChange = (event) => {
    event.preventDefault();
    this.setState({
      tfValue: event.target.value
    })
  }

  constructor(props) {
    super(props);
    console.log(props);
    this.state = {
      tfValue: ""
    }
  }
  render() {
    return (
      <div>
        <Typography
          component="h2"
          variant="h2"
          style={{
            marginTop: 150,
            marginBottom: 50
          }}
        >
          Welcome
        </Typography>
        <TextField label="email" variant="outlined" onChange={this.handleTextFieldChange} value={this.state.tfValue}/>
        <Link to="/dashboard">
          <Button
            variant="contained"
            color="primary"
            size="large"
            style={{height: 56}}
            onClick={this.handleClick}
          >
          Login
          </Button>
        </Link>
      </div>
    )
  }
}

export default Login;