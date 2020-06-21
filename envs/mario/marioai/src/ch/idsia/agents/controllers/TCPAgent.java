package ch.idsia.agents.controllers;

import ch.idsia.benchmark.mario.environments.Environment;

import java.net.*;
import java.io.*;

public class TCPAgent extends BasicMarioAIAgent {
	
	private float last_reward = 0.0f;
	private boolean just_reset = false;
	private ServerSocket server_socket = null;
	private Socket socket = null;
	private DataInputStream rd = null;
	private DataOutputStream wr = null;

	public TCPAgent() {
		super("TCPAgent");
		reset();
		
		// Wait for an incoming connection
		try {
			System.out.println("Waiting for a connection on port 7934...");
			server_socket = new ServerSocket(7934);
			socket = server_socket.accept();
			System.out.println("Connected!");

			rd = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
			wr = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));
		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
	}
	
	public void reset()
	{
	    action = new boolean[Environment.numberOfKeys];
	    just_reset = true;
	}

	public void giveIntermediateReward(float intermediateReward)
	{
		last_reward = intermediateReward;
	}
	
	public boolean[] getAction()
	{
		if (rd == null || wr == null) {
			System.out.println("No network connection");
			return action;
		}

		try {
			// Send an observation to the socket
			wr.writeBoolean(just_reset);
			wr.writeFloat(last_reward);
			wr.writeInt(Environment.numberOfKeys);
			wr.writeInt(receptiveFieldWidth);
			wr.writeInt(receptiveFieldHeight);
			wr.writeBoolean(isMarioOnGround);
			wr.writeBoolean(isMarioAbleToJump);
			
			for (int y=0; y<receptiveFieldHeight; y++) {
				// Tiles and enemies
				wr.write(mergedObservation[y]);
			}
			
			wr.flush();
			
			// Obtain a command back from the controller
			for (int i=0; i<Environment.numberOfKeys; i++) {
				action[i] = rd.readBoolean();
			}
		} catch (IOException e) {
			System.out.println("Reconnecting...");
			
			rd = null;
			wr = null;
			
			try {
				socket = server_socket.accept();
				System.out.println("Connected!");
	
				rd = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
				wr = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));
			} catch (IOException f) {
				System.out.println(f.getMessage());
			}
		}
		
		just_reset = false;

	    return action;
	}
}
