import { Account, ec, json, stark, Provider, hash, CallData, RpcProvider } from "starknet";
import fs from "fs";
import axios from "axios";
import { version } from "os";

// connect provider
// const provider = new Provider({ sequencer: { baseUrl: "http://127.0.0.1:5050" } });
const provider = new Provider({rpc: {nodeUrl: "https://starknet-goerli.infura.io/v3/="}})

// initialize existing predeployed account 0 of Devnet
const privateKey0 = "";
const accountAddress0 = "";
const account0 = new Account(provider, accountAddress0, privateKey0, '1');

// new account abstraction :
// Generate public and private key pair.
const AAprivateKey = stark.randomAddress();
console.log('New account :\nprivateKey=', AAprivateKey);
const AAstarkKeyPub = ec.starkCurve.getStarkKey(AAprivateKey);
console.log('publicKey=', AAstarkKeyPub);
const customerKey = ec.starkCurve.getStarkKey('');
const botKey = ec.starkCurve.getStarkKey('');

console.log('customer key=', customerKey);
console.log('bot key=', botKey);

// declare the contract
const compiledAAaccount = json.parse(fs.readFileSync("aa_workshop_Account.sierra.json").toString("ascii"));
const compiledAAaccountcasm = json.parse(fs.readFileSync("/aa_workshop_Account.casm.json").toString("ascii"));
const { transaction_hash: declTH, class_hash: decCH } =
    await account0.declare({contract: compiledAAaccount, casm: compiledAAaccountcasm});
console.log('Customized account class hash =', decCH);
await provider.waitForTransaction(declTH);

// Calculate future address of the account
const AAaccountConstructorCallData = CallData.compile({
    customer: customerKey,
    bot: botKey
});
const AAcontractAddress = hash.calculateContractAddressFromHash(
    AAstarkKeyPub,
    decCH,
    AAaccountConstructorCallData,
    0
);
console.log('Precalculated account address=', AAcontractAddress);

// deploy account
const AAaccount = new Account(provider, AAcontractAddress, AAprivateKey, '1');
const { transaction_hash, contract_address } = await AAaccount.deployAccount({
    classHash: decCH,
    constructorCalldata: AAaccountConstructorCallData,
    addressSalt: AAstarkKeyPub,
});
await provider.waitForTransaction(transaction_hash);
console.log('✅ New customized account created.\n   address =', contract_address);
