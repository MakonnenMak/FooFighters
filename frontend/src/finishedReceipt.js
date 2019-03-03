// import React, { Component } from 'react';
// import Typography from '@material-ui/core/Typography';
// import TextField from '@material-ui/core/TextField';
// import Button from '@material-ui/core/Button';
// import PropTypes from 'prop-types';
// import { withStyles } from '@material-ui/core/styles';
// import Paper from '@material-ui/core/Paper';
// import Divider from '@material-ui/core/Divider';
// import Grid from '@material-ui/core/Grid';
// import { spacing } from '@material-ui/system';
// import FormGroup from '@material-ui/core/FormGroup';

// class Finished extends Component {
//   render() {
//     return (
//       <div>
        
//         <div style={{ gridRowStart: '10', gridRowEnd: 'span 8', gridColumnStart: '7', gridColumnEnd: 'span 5' }}>
//           <p>
//           <TextField label="price" variant="outlined"/></p><p>Num items claimed</p>
//         </div>

//       </div>
//     )
//   }
// }

// export default Finished;

import React from 'react';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
  container: {
    display: 'grid',
    gridTemplateColumns: 'repeat(12, 1fr)',    
    gridTemplateRows: 'repeat(12, 1fr)',
    gridGap: `${theme.spacing.unit * 5}px`,
  },
  divider: {
    margin: `${theme.spacing.unit * 2}px 0`,
  },
});

const textFieldStyle = {
  width: 500,
  margin: "0 auto",
  marginTop: 250
};

function CSSGrid(props) {
  const { classes } = props;

  return (
    <div className={classes.root}>

        <div style={{ gridRowStart: '4', gridRowEnd: 'span 8', gridColumnStart: '2', gridColumnEnd: 'span 6' }}>

      <Typography variant="h2" style = {textFieldStyle} gutterBottom>
        Receipt Submitted
      </Typography>
      

      <Typography variant="h4" gutterBottom>
              </Typography>
      <Typography variant="h5" gutterBottom>
               You owe $___

      </Typography>

      <Typography variant="subtitle1" gutterBottom>
        Please Venmo @____ by the end of this week. 
      </Typography>
      </div>
    </div>
  );
}

CSSGrid.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CSSGrid);
