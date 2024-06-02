import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';
//import { makeStyles } from '@mui/system';



/* 
const useStyles = makeStyles((theme) => {
    appBar: {
        //customizing the materialui
        borderBottom: `1px solid ${theme.palette.divider}`
    }
}) */

function Header() {
    //const classes = useStyles
    
    return (
        <div>
        {/*     <CssBaseline/>
            <AppBar
            position='static'
            color='white'
            elevation={0}
           // className={classes.appBar}
            >
                <Toolbar>
                    <Typography variant='h6' color={'inherit'} noWrap>
                        BlogmeUp
                    </Typography>
                </Toolbar>
            </AppBar> */}
            <h1>Blaise is my name</h1>
        </div>
    );
}

export default Header;