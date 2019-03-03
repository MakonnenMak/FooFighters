import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

class Login extends Component {
  render() {
    return (
      <div>
        <Typography component="h2" variant="h2">Welcome</Typography>
        <TextField label="email" variant="outlined"/>
        <Button
          variant="contained"
          color="primary"
          size="large"
          style={{height: 56}}
        >
        Login
        </Button>
      </div>
    )
  }
}

export default Login;