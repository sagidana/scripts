defmodule Box do
  def helper(value) do
    value + 1
  end

  def greet(value) do
    helper(value) * 2
  end

  def runner do
    greet(3)
  end
end
