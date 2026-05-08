IMAGE_NAME = manipulation_node
CONTAINER_NAME = manipulation_node

.PHONY: build run shell stop clean

build:
	docker build -t $(IMAGE_NAME):latest .

run: build
	docker run --rm -it --privileged --network host \
		--env DISPLAY=$(DISPLAY) \
		--env QT_X11_NO_MITSHM=1 \
		--volume /tmp/.X11-unix:/tmp/.X11-unix \
		--volume /dev/bus/usb:/dev/bus/usb \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME):latest

shell: build
	docker run --rm -it --privileged --network host \
		--env DISPLAY=$(DISPLAY) \
		--env QT_X11_NO_MITSHM=1 \
		--volume /tmp/.X11-unix:/tmp/.X11-unix \
		--volume /dev/bus/usb:/dev/bus/usb \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME):latest bash

stop:
	docker rm -f $(CONTAINER_NAME) || true

clean:
	docker rmi $(IMAGE_NAME):latest || true
