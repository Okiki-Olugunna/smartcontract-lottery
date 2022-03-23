from brownie import Lottery, config, network
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery! :)")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery has started folks!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("Congrats on entering the lottery. Good luck ;)")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract to call the requestRandomness function
    fund_with_link(lottery.address)
    tx.wait(1)
    # end the lottery
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(59)
    print(
        f"And the new winner is...\n drumroll please...\n {lottery.recentWinner}! \n Congratulations!"
    )


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
