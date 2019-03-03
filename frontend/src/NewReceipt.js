import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormGroup from '@material-ui/core/FormGroup';
import Webcam from 'react-webcam';

const textFieldStyle = {
  width: 500,
  margin: "0 auto",
  marginTop: 20
};

const videoConstraints = {
      width: 1280,
      height: 720,
      facingMode: {exact: "environment"},
};

class NewReceipt extends Component {
  setRef = webcam => {
    this.webcam = webcam;
  };

  render() {
    return (
      <div>
        <Webcam
          audio={false}
          ref={this.setRef}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
        />
        <Typography component="h2" variant="h2">New Receipt</Typography>
        <FormGroup>
          <TextField label="Name" variant="outlined" style={textFieldStyle}/>
          <TextField label="Venmo Id" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 1 email" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 2 email" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 3 email" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 4 email" variant="outlined" style={textFieldStyle}/>
          <TextField label="Recepient 5 email" variant="outlined" style={{...textFieldStyle, marginBottom: 20}}/>
        </FormGroup>
        <Button
          variant="contained"
          color="primary"
          size="large"
        >
        Next
        </Button>
      </div>
    );
  }
}

export default NewReceipt;