CC = /usr/bin/g++

LD_FLAGS = -lrt

### CUDA

CUDA_PATH       ?= /usr/local/cuda
CUDA_INC_PATH   ?= $(CUDA_PATH)/include
CUDA_BIN_PATH   ?= $(CUDA_PATH)/bin
CUDA_LIB_PATH   ?= $(CUDA_PATH)/lib

# CUDA code generation flags
GENCODE_FLAGS   := -gencode arch=compute_20,code=sm_20 -gencode arch=compute_30,code=sm_30 -gencode arch=compute_35,code=sm_35

# Common binaries
NVCC            ?= $(CUDA_BIN_PATH)/nvcc

# OS-specific build flags
ifeq ($(shell uname),Darwin)
        LDFLAGS       := -Xlinker -rpath $(CUDA_LIB_PATH) -L$(CUDA_LIB_PATH) -lcudart -lcufft -lsndfile
        CCFLAGS           := -arch $(OS_ARCH)
else
        ifeq ($(OS_SIZE),32)
                LDFLAGS   := -L$(CUDA_LIB_PATH) -lcudart -lcufft -lsndfile
                CCFLAGS   := -m32
        else
                CUDA_LIB_PATH := $(CUDA_LIB_PATH)64
                LDFLAGS       := -L$(CUDA_LIB_PATH) -lcudart -lcufft -lsndfile
                CCFLAGS       := -m64
        endif
endif

# OS-architecture specific flags
ifeq ($(OS_SIZE),32)
      NVCCFLAGS := -m32 -lcufft
else
      NVCCFLAGS := -m64 -lcufft
endif

###

TARGETS_CPU = sa msa
TARGETS_GPU = cuda_sa cuda_msa

all: $(TARGETS_GPU) $(TARGETS_CPU)

sa: src/sequence_alignment.cpp src/utils.cpp
	$(CC) $^ -o $@ $(LD_FLAGS) -Wall

msa: src/multiple_sequence_alignment.cpp src/utils.cpp
	$(CC) $^ -o $@ $(LD_FLAGS) -Wall

clean_cpu:
	rm -f *.o $(TARGETS_CPU)

clean_gpu:
	rm -f *.0 $(TARGETS_GPU)

clean_all: clean_cpu clean_gpu
