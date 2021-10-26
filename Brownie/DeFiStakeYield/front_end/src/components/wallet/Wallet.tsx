import {Token} from "../Main";
import {Box, Tab} from "@material-ui/core";
import {useState} from "react";
import {TabContext, TabList, TabPanel} from "@mui/lab";
import WalletBalance from "./WalletBalance";
import StakeForm from "./StakeForm";

interface WalletProps {
    supportedTokens: Array<Token>
}

const Wallet = ({supportedTokens}: WalletProps) => {
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0);
    const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        setSelectedTokenIndex(parseInt(newValue));
    }
    return (
        <Box>
            <h1>Wallet</h1>
            <Box>
                <TabContext value={selectedTokenIndex.toString()}>
                    <TabList aria-label={"Stake Form Tabs"} onChange={handleChange}>
                        {
                            supportedTokens.map((token: Token, index: number) => {
                                return (
                                    <Tab label={token.name} value={index.toString()} key={index}/>
                                )
                            })
                        }
                    </TabList>
                    {
                        supportedTokens.map((token: Token, index: number) => {
                            return <TabPanel value={index.toString()} key={index}>
                                <div>
                                    <WalletBalance token={token}/>
                                    <StakeForm token={token}/>
                                </div>
                            </TabPanel>
                        })
                    }
                </TabContext>
            </Box>
        </Box>
    );
}

export default Wallet;