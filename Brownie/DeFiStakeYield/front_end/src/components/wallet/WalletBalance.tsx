import {Token} from "../Main";
import {useEthers, useTokenBalance} from "@usedapp/core";
import {formatUnits} from "ethers/lib/utils";
import BalanceMessage from "./BalanceMessage";

interface WalletBalanceProps {
    token: Token
}

const WalletBalance = ({token}: WalletBalanceProps) => {
    const {image, address, name} = token;
    const {account} = useEthers();
    // Returns a Balance of a given Token for a given Address
    const tokenBalance = useTokenBalance(address, account);
    const formattedTokenBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0;
    return (
        <BalanceMessage
            label={`Un-staked ${name} Balance`}
            tokenImage={image}
            balance={formattedTokenBalance}
        />
    );
}

export default WalletBalance;