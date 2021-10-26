import {Token} from "../Main";
import {useEthers, useNotifications, useTokenBalance} from "@usedapp/core";
import {formatUnits} from "ethers/lib/utils";
import {Button, CircularProgress, Input, Snackbar} from "@material-ui/core";
import {useEffect, useState} from "react";
import useStakeTokens from "../../hooks/useStakeTokens";
import {utils} from "ethers";
import {Alert} from "@mui/lab";

interface StakeFormProps {
    token: Token
}

const StakeForm = ({token}: StakeFormProps) => {
    const {address, name} = token;
    const {account} = useEthers();
    const tokenBalance = useTokenBalance(address, account);
    const formattedTokenBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0;
    const [amount, setAmount] = useState<number>(0);
    const handleAmountChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newAmount = event.target.value === "" ? 0 : Number(event.target.value);
        setAmount(newAmount);
    }
    /* Using Custom Hook to interact with smart Contract - It returns a Function and the State of these Function */
    const {approveAndStake, state: approveAndStakeErc20State} = useStakeTokens(address);
    const handleStakeSubmit = () => {
        const amountAsWei = utils.parseEther(amount.toString());
        return approveAndStake(amountAsWei.toString());
    }
    /* Appending approve and stake Transactions into a Block */
    const isMining = approveAndStakeErc20State.status === "Mining";
    const [showErc20ApprovalSuccess, setShowErc20ApprovalSuccess] = useState(false);
    const [showStakeTokenSuccess, setShowStakeTokenSuccess] = useState(false);
    const {notifications} = useNotifications();
    /* useEffect runs when Notifications change - Notifications are from the Wallet (for Example: approved or succeeded Transactions) */
    useEffect(() => {
        /* Filtering Approve Notifications */
        if (notifications.filter((notification) => {
            /* Return Notification fi Type is "transactionSucceed" and Name is "Approve ERC20 Transfer" */
            return (
                notification.type === "transactionSucceed" &&
                (notification.transactionName === "Approve ERC20 Transfer")
            );
        }).length > 0) {
            setShowErc20ApprovalSuccess(true);
            setShowStakeTokenSuccess(false);
        }
        /* Filtering Stake Notifications */
        if (notifications.filter((notification) => {
            /* Return Notification fi Type is "transactionSucceed" and Name is "Stake Tokens" */
            return (
                notification.type === "transactionSucceed" &&
                (notification.transactionName === "Stake Tokens")
            );
        }).length > 0) {
            setShowErc20ApprovalSuccess(false);
            setShowStakeTokenSuccess(true);
        }
    }, [notifications, showErc20ApprovalSuccess, showStakeTokenSuccess]);
    const handleCloseSnackbar = () => {
        setShowErc20ApprovalSuccess(false);
        setShowStakeTokenSuccess(false);
    }
    return (
        <>
            <Input onChange={handleAmountChange}/>
            <Button
                color={"primary"}
                size={"large"}
                onClick={handleStakeSubmit}
                disabled={isMining}
            >
                {
                    isMining ? (
                        <CircularProgress size={32}/>
                    ) : (
                        <b>Stake</b>
                    )
                }
            </Button>
            <Snackbar open={showErc20ApprovalSuccess} autoHideDuration={4000} onClose={handleCloseSnackbar}>
                <Alert onClose={handleCloseSnackbar} severity={"success"}>ERC20 Token approved</Alert>
            </Snackbar>
            <Snackbar open={showStakeTokenSuccess} autoHideDuration={4000} onClose={handleCloseSnackbar}>
                <Alert onClose={handleCloseSnackbar} severity={"success"}>ERC20 Token staked</Alert>
            </Snackbar>
        </>
    );
}

export default StakeForm;