// Copyright 2014 theaigames.com (developers@theaigames.com)

//    Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at

//        http://www.apache.org/licenses/LICENSE-2.0

//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//    See the License for the specific language governing permissions and
//    limitations under the License.
//	
//    For the full copyright and license information, please view the LICENSE
//    file that was distributed with this source code.

package frontLineBot;

import java.util.ArrayList;
import java.util.LinkedList;

import main.Region;
import move.AttackTransferMove;
import move.PlaceArmiesMove;

public class BotVars implements Bot 
{
	
	public int minAttackNum = 5;
	public int attackNumDivisor = 2;
	public int minTransNum = 1;
	public int[] startingRegions = new int[6];
	
	public BotVars() {}
	
	public BotVars (int minAttackNum, int attackNumDivisor, int minTransNum, int[] startingRegions){
		this.minAttackNum = minAttackNum;
		this.attackNumDivisor = attackNumDivisor;
		this.minTransNum = minTransNum;
		this.startingRegions = startingRegions;
	}
	
//	@Override
//	public void setParams(int minAttackNum, int attackNumDivisor, int minTransNum) {
//		System.out.println(super.getClass());
//	}
	
	@Override
	/**
	 * A method used at the start of the game to decide which player start with what Regions. 6 Regions are required to be returned.
	 * This example randomly picks 6 regions from the pickable starting Regions given by the engine.
	 * @return : a list of m (m=6) Regions starting with the most preferred Region and ending with the least preferred Region to start with 
	 */
	public ArrayList<Region> getPreferredStartingRegions(BotState state, Long timeOut)
	{
		int m = startingRegions.length;
		ArrayList<Region> preferredStartingRegions = new ArrayList<Region>();
		for(int i=0; i<m; i++)
		{
			int regionId = startingRegions[i];
			Region region = state.getFullMap().getRegion(regionId);

			if(!preferredStartingRegions.contains(region))
				preferredStartingRegions.add(region);
			else
				i--;
		}
		
		return preferredStartingRegions;
	}


	@Override
	/**
	 * This method is called for at first part of each round. This example puts two armies on random regions
	 * until he has no more armies left to place.
	 * @return The list of PlaceArmiesMoves for one round
	 */
	public ArrayList<PlaceArmiesMove> getPlaceArmiesMoves(BotState state, Long timeOut) 
	{
		
		// ArrayList<PlaceArmiesMove> placeArmiesMoves = new ArrayList<PlaceArmiesMove>();
		// String myName = state.getMyPlayerName();
		// int armies = 2;
		// int armiesLeft = state.getStartingArmies();
		// LinkedList<Region> visibleRegions = state.getVisibleMap().getRegions();
		
		// while(armiesLeft > 0)
		// {
		// 	double rand = Math.random();
		// 	int r = (int) (rand*visibleRegions.size());
		// 	Region region = visibleRegions.get(r);
			
		// 	if(region.ownedByPlayer(myName))
		// 	{
		// 		placeArmiesMoves.add(new PlaceArmiesMove(myName, region, armies));
		// 		armiesLeft -= armies;
		// 	}
		// }

		ArrayList<PlaceArmiesMove> placeArmiesMoves = new ArrayList<PlaceArmiesMove>();
		String myName = state.getMyPlayerName();

		// number of armies left
		int numArmies = state.getStartingArmies();

		// find all regions held by player that is bordering other regions
		LinkedList<Region> visibleRegions = state.getVisibleMap().getRegions();
		LinkedList<Region> borderingRegions = new LinkedList<Region>();

		// current region being checked
		Region current;

		for(int i = 0; i < visibleRegions.size(); i++){

			if(visibleRegions.get(i).ownedByPlayer(myName)){
				
				current = visibleRegions.get(i);

				if(isBorder(current, myName)){
	                borderingRegions.add(current);
				}

			}
		}

        int numToPlace = (int)Math.ceil((double)numArmies/borderingRegions.size());
     
        int i = 0;
		while(numArmies > 0 && borderingRegions.size() > 0){
			placeArmiesMoves.add(new PlaceArmiesMove(myName, borderingRegions.get(i), numToPlace));
			numArmies -= numToPlace;
			i++;
		}

		return placeArmiesMoves;
	}

	private boolean isBorder(Region region, String myName){

			LinkedList<Region> neighbors = region.getNeighbors();

			int numNeighborsChecked = 0;
			while(numNeighborsChecked < neighbors.size()){
				
				if(!neighbors.get(numNeighborsChecked).ownedByPlayer(myName)){

					// add it to list then exit while loop
					return true;
				}
				numNeighborsChecked++;
			}

			return false;
	}



	@Override
	/**
	 * This method is called for at the second part of each round. This example attacks if a region has
	 * more than 6 armies on it, and transfers if it has less than 6 and a neighboring owned region.
	 * @return The list of PlaceArmiesMoves for one round
	 */
	public ArrayList<AttackTransferMove> getAttackTransferMoves(Bot bot, BotState state, Long timeOut) 
	{
		ArrayList<AttackTransferMove> attackTransferMoves = new ArrayList<AttackTransferMove>();
		String myName = state.getMyPlayerName();
		BotVars botVars = (BotVars)bot;
		int minAttackNum = botVars.minAttackNum;
		int attackNumDivisor = botVars.attackNumDivisor;
		int minTransNum = botVars.minTransNum;
		//int armies = 5;
		for(Region fromRegion : state.getVisibleMap().getRegions())
		{
			if(fromRegion.ownedByPlayer(myName)) //do an attack
			{
				ArrayList<Region> possibleToRegions = new ArrayList<Region>();
				possibleToRegions.addAll(fromRegion.getNeighbors());
				
				while(!possibleToRegions.isEmpty())
				{
					double rand = Math.random();
					int r = (int) (rand*possibleToRegions.size());
					Region toRegion = possibleToRegions.get(r);
					
					if(!toRegion.getPlayerName().equals(myName) && fromRegion.getArmies() > minAttackNum) //do an attack
					{
						attackTransferMoves.add(new AttackTransferMove(myName, fromRegion, toRegion, fromRegion.getArmies()/attackNumDivisor));
						break;
					}
					else if(toRegion.getPlayerName().equals(myName) && isBorder(toRegion, myName) && fromRegion.getArmies() > minTransNum) //do a transfer
					{
						if(!isBorder(fromRegion, myName)){
						attackTransferMoves.add(new AttackTransferMove(myName, fromRegion, toRegion, fromRegion.getArmies()-minTransNum));
					}
						break;
					 
					}
					else
						possibleToRegions.remove(toRegion);
				}
			}
		}
		
		return attackTransferMoves;
	}

	public static void main(String[] args)
	{
		int minAttackNum = Integer.parseInt(args[0]);
		int attackNumDivisor = Integer.parseInt(args[1]);
		int minTransNum = Integer.parseInt(args[2]); 
		int startingRegions[] = new int[6];
		startingRegions[0] = Integer.parseInt(args[3]);
		startingRegions[1] = Integer.parseInt(args[4]);
		startingRegions[2] = Integer.parseInt(args[5]);
		startingRegions[3] = Integer.parseInt(args[6]);
		startingRegions[4] = Integer.parseInt(args[7]);
		startingRegions[5] = Integer.parseInt(args[8]);
		
		BotParser parser = new BotParser(new BotVars(minAttackNum, attackNumDivisor, minTransNum, startingRegions));
		parser.run();
	}

}
