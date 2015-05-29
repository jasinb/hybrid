defmodule Hybrid.Router do
  use Hybrid.Web, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", Hybrid do
    pipe_through :browser # Use the default browser stack

    get "/", PageController, :index
  end

  socket "/ws", Hybrid do
    channel "agents:*", AgentChannel
  end
  # Other scopes may use custom stacks.
  # scope "/api", Hybrid do
  #   pipe_through :api
  # end
end
