import {makeStyles} from "@material-ui/core";

interface BalanceMessageProps {
    label: string,
    tokenImage: string,
    balance: number
}

const useStyles = makeStyles((theme) => ({
    container: {
        display: "inline-grid",
        gridTemplateColumns: "auto auto auto",
        gap: theme.spacing(1),
        alignItems: "center"
    },
    tokenImage: {
        width: "32px"
    },
    balance: {
        fontWeight: 700
    }
}));


const BalanceMessage = ({label, tokenImage, balance}: BalanceMessageProps) => {
    const classes = useStyles();

    return (
        <div className={classes.container}>
            <div>{label}</div>
            <div className={classes.balance}>{balance}</div>
            <img className={classes.tokenImage} src={tokenImage} alt={"Token Logo"}/>
        </div>
    );
}

export default BalanceMessage;