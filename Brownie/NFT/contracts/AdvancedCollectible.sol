// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    enum DogBreed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 => DogBreed) public tokenIdToDogBreed;
    mapping(bytes32 => address) public requestIdToSender;
    // Keyword "indexed" just makes it easier to search for this Event
    event CollectibleRequested(bytes32 indexed requestId, address requester);
    event DogBreedAssigned(uint256 indexed tokenId, DogBreed dogBreed);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    ) public VRFConsumerBase(_vrfCoordinator, _linkToken) ERC721("Dogie", "DOG") {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        // Mapping the RequestId to the Creator of that NFT
        requestIdToSender[requestId] = msg.sender;
        emit CollectibleRequested(requestId, msg.sender);
        return requestId;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        DogBreed dogBreed = DogBreed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToDogBreed[newTokenId] = dogBreed;
        emit DogBreedAssigned(newTokenId, dogBreed);
        // msg.sender is going to be the VRF Coordinator cause the VRF Coordinator is calling the Method fulfillRandomness()
        // So a Mapping is used to use the origin Creator as the Owner of the Token
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter++;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // Only Owner of NFT can set the TokenURI
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: Caller ist not Owner nor approved");
        _setTokenURI(tokenId, _tokenURI);
    }
}
