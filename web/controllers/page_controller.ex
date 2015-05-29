defmodule Hybrid.PageController do
  use Hybrid.Web, :controller

  plug :action

  def index(conn, _params) do
    render conn, "index.html"
  end
end
