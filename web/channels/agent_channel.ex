defmodule Hybrid.AgentChannel do
  use Phoenix.Channel

  def join("agents:", _auth_msg, socket) do
     IO.puts "joined channel"
     { :ok, socket }
  end

  def handle_in("agent_update", payload = %{"agent" => agent}, socket) do
    IO.puts "Update from agent " <> agent
    IO.inspect payload
    IO.puts ""
    broadcast! socket, "agent_update", payload
    {:noreply, socket}
  end
end
