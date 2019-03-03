// import React, { Component } from 'react';
// import Typography from '@material-ui/core/Typography';
// import TextField from '@material-ui/core/TextField';
// import Button from '@material-ui/core/Button';

// class Select extends Component {
//   render() {
//     return (
//       <div>
//         <Typography component="h2" variant="h2">Welcome</Typography>
//         <TextField label="email" variant="outlined"/>
//         <Button
//           variant="contained"
//           color="primary"
//           size="large"
//           style={{height: 56}}
//         >
//         Login
//         </Button>
//       </div>
//     )
//   }
// }

// export default Select;

import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Divider from '@material-ui/core/Divider';
import Grid from '@material-ui/core/Grid';
import { spacing } from '@material-ui/system';

const styles = theme => ({
  container: {
    display: 'grid',
    gridTemplateColumns: 'repeat(12, 1fr)',    
    gridTemplateRows: 'repeat(12, 1fr)',
    gridGap: `${theme.spacing.unit * 5}px`,
  },
  paper: {
    padding: theme.spacing.unit,
    textAlign: 'center',
    color: theme.palette.text.secondary,
    whiteSpace: 'nowrap',
    marginBottom: theme.spacing.unit,
  },
  divider: {
    margin: `${theme.spacing.unit * 2}px 0`,
  },
});

function CSSGrid(props) {
  const { classes } = props;

  return (

    <div>

      <div>
        <div>
          <p>  </p>
        </div>
        <Button
          variant="contained"
          color="primary"
          size="large"
          style={{height: 50}, {fontSize: '20px'}}
        >
        Homepage
        </Button>
      </div>
        <Divider className={classes.divider} />

      <div className={classes.container}>
        <div style={{ gridRowStart: '1', gridRowEnd: 'span 8', gridColumnStart: '1', gridColumnEnd: 'span 6' }}>
          <Paper className={classes.paper} style={{fontSize: '30px'}}>yeet<p>yeet yeet</p><p>yeet yeet yeet</p><p>Yeet plz just put ur receipts in here</p></Paper>
        </div>

        <div style={{ gridRowStart: '4', gridRowEnd: 'span 8', gridColumnStart: '7', gridColumnEnd: 'span 5' }}>
          <Paper className={classes.paper} style={{fontSize: '30px'}}>yeet<p>yeet yeet</p><p>yeet yeet yeet</p><p>Yeet plz just put ur answers</p></Paper>
        </div>

        <div style={{ gridRowStart: '11', gridRowEnd: 'span 8', gridColumnStart: '7', gridColumnEnd: 'span 5' }}>
          <p> Num items you've claimed:</p>
          </div>
      </div>
    </div>
  );
}

CSSGrid.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CSSGrid);
