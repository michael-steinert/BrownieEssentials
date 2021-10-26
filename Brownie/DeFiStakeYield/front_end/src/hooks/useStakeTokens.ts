import {useContractFunction, useEthers} from "@usedapp/core";
import {constants, Contract, utils} from "ethers";
import {useEffect, useState} from "react";
import TokenFarm from "./abis/TokenFarm.json"
import ERC20 from "./abis/MockERC20.json"

const useStakeTokens = (tokenAddress: string) => {
    const {chainId} = useEthers();
    const {tokenFarmABI} = TokenFarm;
    const {erc20ABI} = ERC20;
    const tokenFarmAddress = chainId ? "" : constants.AddressZero;
    const tokenFarmInterface = new utils.Interface(tokenFarmABI);
    const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface);
    const erc20Interface = new utils.Interface(erc20ABI);
    const erc20Contract = new Contract(tokenAddress, erc20Interface);

    /* Calling approve() of ERC20 Contract */
    const {send: approveErc20Send, state: approveAndStakeErc20State} = useContractFunction(
        erc20Contract,
        "approve",
        {transactionName: "Approve ERC20 Transfer"}
    );
    const approveAndStake = (amount: string) => {
        /* Changing Variable runs the useEffect Hook to stake the Amount */
        setAmountToStake(amount);
        return approveErc20Send(tokenFarmAddress, amount);
    }

    /* Defining stake() of Smart Contract */
    const {send: stakeSend, state: stakeState} = useContractFunction(
        tokenFarmContract,
        "stakeTokens",
        {transactionName: "Stake Tokens"}
    );
    const [amountToStake, setAmountToStake] = useState<string>("0");

    // useEffect is called when a Variable has been changed - when Transaction was successfully the Variable approveErc20State changes
    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            /* Calling stake() of TokenFarm Contract */
            stakeSend(amountToStake, tokenAddress);
        }
    }, [approveAndStakeErc20State]);

    /* Tracking the Status of approve and stake Functions of Contract*/
    const [state, setState] = useState(approveAndStakeErc20State);
    useEffect(() => {
        /* If approve Transaction is successful the State depends on the stake Transaction */
        if (approveAndStakeErc20State.status === "Success") {
            setState(stakeState);
        } else {
            setState(approveAndStakeErc20State);
        }
    }, [approveAndStakeErc20State, stakeState]);
    return {approveAndStake, state}
}

export default useStakeTokens;
