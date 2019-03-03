import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import { Link } from 'react-router-dom';

class Login extends Component {
  render() {
    return (
      <div>
        <Typography component="h2" variant="h2">Welcome</Typography>
        <TextField label="email" variant="outlined"/>
        <Link to="/dashboard">
          <Button
            variant="contained"
            color="primary"
            size="large"
            style={{height: 56}}
          >
          Login
          </Button>
        </Link>
      </div>
    )
  }
}

export default Login;