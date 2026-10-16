<?php

declare(strict_types=1);

class SessionHandlerAdapter implements SessionHandlerInterface
{

	public function __construct(
		private CakeSessionHandlerInterface $cakeSessionHandler
	) {
	}

	#[\ReturnTypeWillChange]
	public function close()
	{
		return $this->cakeSessionHandler->close();
	}

	#[\ReturnTypeWillChange]
	public function destroy(string $id)
	{
		return $this->cakeSessionHandler->destroy($id);
	}

	#[\ReturnTypeWillChange]
	public function gc(int $max_lifetime)
	{
		return $this->cakeSessionHandler->gc($max_lifetime);
	}

	#[\ReturnTypeWillChange]
	public function open(string $path, string $name)
	{
		//Cake interface ignores these parameters.
		return $this->cakeSessionHandler->open();
	}

	#[\ReturnTypeWillChange]
	public function read(string $id)
	{
		return $this->cakeSessionHandler->read($id);
	}

	#[\ReturnTypeWillChange]
	public function write(string $id, string $data)
	{
		return $this->cakeSessionHandler->write($id, $data);
	}
}
