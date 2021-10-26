import {useEthers} from "@usedapp/core";
import {constants} from "ethers";
import Wallet from "./wallet/Wallet";
import {makeStyles} from "@material-ui/core";

export type Token = {
    image: string
    address: string
    name: string
}

const useStyles = makeStyles((theme) => ({
    title: {
        color: theme.palette.common.white,
        textAlign: "center",
        padding: theme.spacing(4)
    }
}));

const Main = () => {
    const classes = useStyles();
    const {chainId, error} = useEthers();
    const networkName = chainId ? "" : "dev";
    const dAppTokenAddress = chainId ? "" : constants.AddressZero;
    const supportedTokens: Array<Token> = [
        {
            image: "",
            address: dAppTokenAddress,
            name: "DAPP"
        }
    ];
    return (
        <>
            <h2 className={classes.title}>DApp Token App</h2>
            <Wallet supportedTokens={supportedTokens}/>
        </>
    );
}

export default Main;