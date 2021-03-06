---

title:  "Stencil 3D r1 star constant homogeneous double Zen_EPYC-7451"

dimension    : "3D"
radius       : "r1"
weighting    : "homogeneous"
kind         : "star"
coefficients : "constant"
datatype     : "double"
machine      : "Zen_EPYC-7451"
compile_flags: "icc -O3 -xHost -fno-alias -qopenmp"
flop         : "7"
scaling      : [ "760" ]
blocking     : []
---

{%- capture basename -%}
{{page.dimension}}-{{page.radius}}-{{page.weighting}}-{{page.kind}}-{{page.coefficients}}-{{page.datatype}}-{{page.machine}}
{%- endcapture -%}

{%- capture source_code -%}
double a[M][N][P];
double b[M][N][P];
double c0;

for(long k=1; k < M-1; ++k){
for(long j=1; j < N-1; ++j){
for(long i=1; i < P-1; ++i){
b[k][j][i] = c0 * (a[k][j][i]
+ a[k][j][i-1] + a[k][j][i+1]
+ a[k-1][j][i] + a[k+1][j][i]
+ a[k][j-1][i] + a[k][j+1][i]
);
}
}
}
{%- endcapture -%}
{%- capture source_code_asm -%}
P vmovupd   8(%r10,%r8,8), %ymm3
P vmovupd   8(%rsi,%r8,8), %xmm5
P vmovupd   8(%rdx,%r8,8), %xmm8
P vaddpd    (%r10,%r8,8), %ymm3, %ymm4
vmovupd   8(%rdi,%r8,8), %xmm11
vaddpd    16(%r10,%r8,8), %ymm4, %ymm6
vmovupd   8(%r9,%r8,8), %xmm14
vinsertf128 $1, 24(%rsi,%r8,8), %ymm5, %ymm7
vaddpd    %ymm7, %ymm6, %ymm9
vinsertf128 $1, 24(%rdx,%r8,8), %ymm8, %ymm10
vaddpd    %ymm10, %ymm9, %ymm12
vmovupd   40(%rsi,%r8,8), %xmm8
vinsertf128 $1, 24(%rdi,%r8,8), %ymm11, %ymm13
vaddpd    %ymm13, %ymm12, %ymm15
vmovupd   40(%rdx,%r8,8), %xmm11
vinsertf128 $1, 24(%r9,%r8,8), %ymm14, %ymm3
vaddpd    %ymm3, %ymm15, %ymm4
vmovupd   40(%rdi,%r8,8), %xmm14
vmulpd    %ymm4, %ymm1, %ymm5
vmovupd   40(%r9,%r8,8), %xmm4
vmovupd   %ymm5, 8(%r14,%r8,8)
vmovupd   40(%r10,%r8,8), %ymm6
vaddpd    32(%r10,%r8,8), %ymm6, %ymm7
vaddpd    48(%r10,%r8,8), %ymm7, %ymm9
vinsertf128 $1, 56(%rsi,%r8,8), %ymm8, %ymm10
vaddpd    %ymm10, %ymm9, %ymm12
vinsertf128 $1, 56(%rdx,%r8,8), %ymm11, %ymm13
vaddpd    %ymm13, %ymm12, %ymm15
vmovupd   72(%rsi,%r8,8), %xmm11
vinsertf128 $1, 56(%rdi,%r8,8), %ymm14, %ymm3
vaddpd    %ymm3, %ymm15, %ymm5
vmovupd   72(%rdx,%r8,8), %xmm14
vinsertf128 $1, 56(%r9,%r8,8), %ymm4, %ymm6
vaddpd    %ymm6, %ymm5, %ymm7
vmovupd   72(%rdi,%r8,8), %xmm4
vmulpd    %ymm7, %ymm1, %ymm8
vmovupd   72(%r9,%r8,8), %xmm7
vmovupd   %ymm8, 40(%r14,%r8,8)
vmovupd   72(%r10,%r8,8), %ymm9
vaddpd    64(%r10,%r8,8), %ymm9, %ymm10
vaddpd    80(%r10,%r8,8), %ymm10, %ymm12
vinsertf128 $1, 88(%rsi,%r8,8), %ymm11, %ymm13
vaddpd    %ymm13, %ymm12, %ymm15
vinsertf128 $1, 88(%rdx,%r8,8), %ymm14, %ymm3
vaddpd    %ymm3, %ymm15, %ymm5
vmovupd   104(%rsi,%r8,8), %xmm14
vinsertf128 $1, 88(%rdi,%r8,8), %ymm4, %ymm6
vaddpd    %ymm6, %ymm5, %ymm8
vmovupd   104(%rdx,%r8,8), %xmm4
vinsertf128 $1, 88(%r9,%r8,8), %ymm7, %ymm9
vaddpd    %ymm9, %ymm8, %ymm10
vmovupd   104(%rdi,%r8,8), %xmm7
vmulpd    %ymm10, %ymm1, %ymm11
vmovupd   104(%r9,%r8,8), %xmm10
vmovupd   %ymm11, 72(%r14,%r8,8)
vmovupd   104(%r10,%r8,8), %ymm12
vaddpd    96(%r10,%r8,8), %ymm12, %ymm13
vaddpd    112(%r10,%r8,8), %ymm13, %ymm15
* .byte     144
vinsertf128 $1, 120(%rsi,%r8,8), %ymm14, %ymm3
vaddpd    %ymm3, %ymm15, %ymm5
vinsertf128 $1, 120(%rdx,%r8,8), %ymm4, %ymm6
vaddpd    %ymm6, %ymm5, %ymm8
vinsertf128 $1, 120(%rdi,%r8,8), %ymm7, %ymm9
vaddpd    %ymm9, %ymm8, %ymm11
vinsertf128 $1, 120(%r9,%r8,8), %ymm10, %ymm12
vaddpd    %ymm12, %ymm11, %ymm13
vmulpd    %ymm13, %ymm1, %ymm14
vmovupd   %ymm14, 104(%r14,%r8,8)
addq      $16, %r8
cmpq      %r11, %r8
jb        ..B1.16
{%- endcapture -%}

{%- capture layercondition -%}
L1: unconditionally fulfilled
L2: unconditionally fulfilled
L3: unconditionally fulfilled
L1: P <= 2050/3;P ~ 680
L2: P <= 32770/3;P ~ 10920
L3: P <= 524290/3;P ~ 174760
L1: 16*N*P + 16*P*(N - 1) <= 32768;N*P ~ 30²
L2: 16*N*P + 16*P*(N - 1) <= 524288;N*P ~ 120²
L3: 16*N*P + 16*P*(N - 1) <= 8388608;N*P ~ 510²
{%- endcapture -%}
{%- capture iaca -%}

Throughput Analysis Report
--------------------------
P - Load operation can be hidden behind a past or future store instruction
X - No information for this instruction in data file
* - Not bound to a port, therefore ignored


Port Binding in Cycles Per Iteration:
-----------------------------------------------------------------------------------
|  Port  |  0   |  1   |  2   |   3   | 3DV |  4  |  5  |  6  |  7  |  8   |  9   |
-----------------------------------------------------------------------------------
| Cycles | 9.28 | 9.28 | 24.0 | 29.28 |  0  | 0.5 | 0.5 | 0.5 | 0.5 | 28.5 | 28.5 |
-----------------------------------------------------------------------------------


                           Ports Pressure in cycles
|  0   |  1   |  2   |  3   | 3DV  |  4   |  5   |  6   |  7   |  8   |  9   |
------------------------------------------------------------------------------
|      |      |      |      |      |      |      |      |      |      |      | P vmovupd   8(%r10,%r8,8), %ymm3
|      |      |      |      |      |      |      |      |      |      |      | P vmovupd   8(%rsi,%r8,8), %xmm5
|      |      |      |      |      |      |      |      |      |      |      | P vmovupd   8(%rdx,%r8,8), %xmm8
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | P vaddpd    (%r10,%r8,8), %ymm3, %ymm4
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   8(%rdi,%r8,8), %xmm11
|      |      | 1.00 | 1.00 |      |      |      |      |      | 0.50 | 0.50 | vaddpd    16(%r10,%r8,8), %ymm4, %ymm6
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   8(%r9,%r8,8), %xmm14
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 24(%rsi,%r8,8), %ymm5, %ymm7
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm7, %ymm6, %ymm9
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 24(%rdx,%r8,8), %ymm8, %ymm10
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm10, %ymm9, %ymm12
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   40(%rsi,%r8,8), %xmm8
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 24(%rdi,%r8,8), %ymm11, %ymm13
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm13, %ymm12, %ymm15
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   40(%rdx,%r8,8), %xmm11
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 24(%r9,%r8,8), %ymm14, %ymm3
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm3, %ymm15, %ymm4
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   40(%rdi,%r8,8), %xmm14
| 1.00 | 1.00 |      |      |      |      |      |      |      |      |      | vmulpd    %ymm4, %ymm1, %ymm5
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   40(%r9,%r8,8), %xmm4
|      |      |      |      |      |      |      |      |      | 2.00 | 2.00 | vmovupd   %ymm5, 8(%r14,%r8,8)
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   40(%r10,%r8,8), %ymm6
|      |      | 1.00 | 1.00 |      |      |      |      |      | 0.50 | 0.50 | vaddpd    32(%r10,%r8,8), %ymm6, %ymm7
|      |      | 1.00 | 1.00 |      |      |      |      |      | 0.50 | 0.50 | vaddpd    48(%r10,%r8,8), %ymm7, %ymm9
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 56(%rsi,%r8,8), %ymm8, %ymm10
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm10, %ymm9, %ymm12
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 56(%rdx,%r8,8), %ymm11, %ymm13
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm13, %ymm12, %ymm15
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   72(%rsi,%r8,8), %xmm11
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 56(%rdi,%r8,8), %ymm14, %ymm3
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm3, %ymm15, %ymm5
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   72(%rdx,%r8,8), %xmm14
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 56(%r9,%r8,8), %ymm4, %ymm6
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm6, %ymm5, %ymm7
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   72(%rdi,%r8,8), %xmm4
| 1.00 | 1.00 |      |      |      |      |      |      |      |      |      | vmulpd    %ymm7, %ymm1, %ymm8
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   72(%r9,%r8,8), %xmm7
|      |      |      |      |      |      |      |      |      | 2.00 | 2.00 | vmovupd   %ymm8, 40(%r14,%r8,8)
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   72(%r10,%r8,8), %ymm9
|      |      | 1.00 | 1.00 |      |      |      |      |      | 0.50 | 0.50 | vaddpd    64(%r10,%r8,8), %ymm9, %ymm10
|      |      | 1.00 | 1.00 |      |      |      |      |      | 0.50 | 0.50 | vaddpd    80(%r10,%r8,8), %ymm10, %ymm12
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 88(%rsi,%r8,8), %ymm11, %ymm13
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm13, %ymm12, %ymm15
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 88(%rdx,%r8,8), %ymm14, %ymm3
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm3, %ymm15, %ymm5
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   104(%rsi,%r8,8), %xmm14
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 88(%rdi,%r8,8), %ymm4, %ymm6
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm6, %ymm5, %ymm8
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   104(%rdx,%r8,8), %xmm4
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 88(%r9,%r8,8), %ymm7, %ymm9
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm9, %ymm8, %ymm10
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   104(%rdi,%r8,8), %xmm7
| 1.00 | 1.00 |      |      |      |      |      |      |      |      |      | vmulpd    %ymm10, %ymm1, %ymm11
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   104(%r9,%r8,8), %xmm10
|      |      |      |      |      |      |      |      |      | 2.00 | 2.00 | vmovupd   %ymm11, 72(%r14,%r8,8)
|      |      |      |      |      |      |      |      |      | 1.00 | 1.00 | vmovupd   104(%r10,%r8,8), %ymm12
|      |      | 1.00 | 1.00 |      |      |      |      |      | 0.50 | 0.50 | vaddpd    96(%r10,%r8,8), %ymm12, %ymm13
|      |      | 1.00 | 1.00 |      |      |      |      |      | 0.50 | 0.50 | vaddpd    112(%r10,%r8,8), %ymm13, %ymm15
|      |      |      |      |      |      |      |      |      |      |      | * .byte     144
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 120(%rsi,%r8,8), %ymm14, %ymm3
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm3, %ymm15, %ymm5
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 120(%rdx,%r8,8), %ymm4, %ymm6
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm6, %ymm5, %ymm8
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 120(%rdi,%r8,8), %ymm7, %ymm9
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm9, %ymm8, %ymm11
| 0.33 | 0.33 |      | 0.33 |      |      |      |      |      |      |      | vinsertf128 $1, 120(%r9,%r8,8), %ymm10, %ymm12
|      |      | 1.00 | 1.00 |      |      |      |      |      |      |      | vaddpd    %ymm12, %ymm11, %ymm13
| 1.00 | 1.00 |      |      |      |      |      |      |      |      |      | vmulpd    %ymm13, %ymm1, %ymm14
|      |      |      |      |      |      |      |      |      | 2.00 | 2.00 | vmovupd   %ymm14, 104(%r14,%r8,8)
|      |      |      |      |      | 0.25 | 0.25 | 0.25 | 0.25 |      |      | addq      $16, %r8
|      |      |      |      |      | 0.25 | 0.25 | 0.25 | 0.25 |      |      | cmpq      %r11, %r8
|      |      |      |      |      |      |      |      |      |      |      | jb        ..B1.16
Total number of estimated throughput: 29.28
{%- endcapture -%}
{%- capture hostinfo -%}

################################################################################
# Hostname
################################################################################
naples1.rrze.uni-erlangen.de

################################################################################
# Operating System
################################################################################
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=18.04
DISTRIB_CODENAME=bionic
DISTRIB_DESCRIPTION="Ubuntu 18.04.2 LTS"
NAME="Ubuntu"
VERSION="18.04.2 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.2 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic

################################################################################
# Operating System (LSB)
################################################################################
No LSB modules are available.

################################################################################
# Operating System Kernel
################################################################################
Linux naples1 4.15.0-45-generic #48-Ubuntu SMP Tue Jan 29 16:28:13 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

################################################################################
# Logged in users
################################################################################
 10:17:19 up 102 days, 18:13,  0 users,  load average: 0.06, 0.02, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT

################################################################################
# CPUset
################################################################################
Domain N:
	0,48,1,49,2,50,3,51,4,52,5,53,6,54,7,55,8,56,9,57,10,58,11,59,12,60,13,61,14,62,15,63,16,64,17,65,18,66,19,67,20,68,21,69,22,70,23,71,24,72,25,73,26,74,27,75,28,76,29,77,30,78,31,79,32,80,33,81,34,82,35,83,36,84,37,85,38,86,39,87,40,88,41,89,42,90,43,91,44,92,45,93,46,94,47,95

Domain S0:
	0,48,1,49,2,50,3,51,4,52,5,53,6,54,7,55,8,56,9,57,10,58,11,59,12,60,13,61,14,62,15,63,16,64,17,65,18,66,19,67,20,68,21,69,22,70,23,71

Domain S1:
	24,72,25,73,26,74,27,75,28,76,29,77,30,78,31,79,32,80,33,81,34,82,35,83,36,84,37,85,38,86,39,87,40,88,41,89,42,90,43,91,44,92,45,93,46,94,47,95

Domain C0:
	0,48,1,49,2,50

Domain C1:
	3,51,4,52,5,53

Domain C2:
	6,54,7,55,8,56

Domain C3:
	9,57,10,58,11,59

Domain C4:
	12,60,13,61,14,62

Domain C5:
	15,63,16,64,17,65

Domain C6:
	18,66,19,67,20,68

Domain C7:
	21,69,22,70,23,71

Domain C8:
	24,72,25,73,26,74

Domain C9:
	27,75,28,76,29,77

Domain C10:
	30,78,31,79,32,80

Domain C11:
	33,81,34,82,35,83

Domain C12:
	36,84,37,85,38,86

Domain C13:
	39,87,40,88,41,89

Domain C14:
	42,90,43,91,44,92

Domain C15:
	45,93,46,94,47,95

Domain M0:
	0,48,1,49,2,50,3,51,4,52,5,53

Domain M1:
	6,54,7,55,8,56,9,57,10,58,11,59

Domain M2:
	12,60,13,61,14,62,15,63,16,64,17,65

Domain M3:
	18,66,19,67,20,68,21,69,22,70,23,71

Domain M4:
	24,72,25,73,26,74,27,75,28,76,29,77

Domain M5:
	30,78,31,79,32,80,33,81,34,82,35,83

Domain M6:
	36,84,37,85,38,86,39,87,40,88,41,89

Domain M7:
	42,90,43,91,44,92,45,93,46,94,47,95


################################################################################
# CGroups
################################################################################
Allowed CPUs: 0-95
Allowed Memory controllers: 0-7

################################################################################
# Topology
################################################################################
--------------------------------------------------------------------------------
CPU name:	AMD EPYC 7451 24-Core Processor
CPU type:	AMD K17 (Zen) architecture
CPU stepping:	2
********************************************************************************
Hardware Thread Topology
********************************************************************************
Sockets:		2
Cores per socket:	24
Threads per core:	2
--------------------------------------------------------------------------------
HWThread	Thread		Core		Socket		Available
0		0		0		0		*
1		0		1		0		*
2		0		2		0		*
3		0		3		0		*
4		0		4		0		*
5		0		5		0		*
6		0		6		0		*
7		0		7		0		*
8		0		8		0		*
9		0		9		0		*
10		0		10		0		*
11		0		11		0		*
12		0		12		0		*
13		0		13		0		*
14		0		14		0		*
15		0		15		0		*
16		0		16		0		*
17		0		17		0		*
18		0		18		0		*
19		0		19		0		*
20		0		20		0		*
21		0		21		0		*
22		0		22		0		*
23		0		23		0		*
24		0		24		1		*
25		0		25		1		*
26		0		26		1		*
27		0		27		1		*
28		0		28		1		*
29		0		29		1		*
30		0		30		1		*
31		0		31		1		*
32		0		32		1		*
33		0		33		1		*
34		0		34		1		*
35		0		35		1		*
36		0		36		1		*
37		0		37		1		*
38		0		38		1		*
39		0		39		1		*
40		0		40		1		*
41		0		41		1		*
42		0		42		1		*
43		0		43		1		*
44		0		44		1		*
45		0		45		1		*
46		0		46		1		*
47		0		47		1		*
48		1		0		0		*
49		1		1		0		*
50		1		2		0		*
51		1		3		0		*
52		1		4		0		*
53		1		5		0		*
54		1		6		0		*
55		1		7		0		*
56		1		8		0		*
57		1		9		0		*
58		1		10		0		*
59		1		11		0		*
60		1		12		0		*
61		1		13		0		*
62		1		14		0		*
63		1		15		0		*
64		1		16		0		*
65		1		17		0		*
66		1		18		0		*
67		1		19		0		*
68		1		20		0		*
69		1		21		0		*
70		1		22		0		*
71		1		23		0		*
72		1		24		1		*
73		1		25		1		*
74		1		26		1		*
75		1		27		1		*
76		1		28		1		*
77		1		29		1		*
78		1		30		1		*
79		1		31		1		*
80		1		32		1		*
81		1		33		1		*
82		1		34		1		*
83		1		35		1		*
84		1		36		1		*
85		1		37		1		*
86		1		38		1		*
87		1		39		1		*
88		1		40		1		*
89		1		41		1		*
90		1		42		1		*
91		1		43		1		*
92		1		44		1		*
93		1		45		1		*
94		1		46		1		*
95		1		47		1		*
--------------------------------------------------------------------------------
Socket 0:		( 0 48 1 49 2 50 3 51 4 52 5 53 6 54 7 55 8 56 9 57 10 58 11 59 12 60 13 61 14 62 15 63 16 64 17 65 18 66 19 67 20 68 21 69 22 70 23 71 )
Socket 1:		( 24 72 25 73 26 74 27 75 28 76 29 77 30 78 31 79 32 80 33 81 34 82 35 83 36 84 37 85 38 86 39 87 40 88 41 89 42 90 43 91 44 92 45 93 46 94 47 95 )
--------------------------------------------------------------------------------
********************************************************************************
Cache Topology
********************************************************************************
Level:			1
Size:			32 kB
Cache groups:		( 0 48 ) ( 1 49 ) ( 2 50 ) ( 3 51 ) ( 4 52 ) ( 5 53 ) ( 6 54 ) ( 7 55 ) ( 8 56 ) ( 9 57 ) ( 10 58 ) ( 11 59 ) ( 12 60 ) ( 13 61 ) ( 14 62 ) ( 15 63 ) ( 16 64 ) ( 17 65 ) ( 18 66 ) ( 19 67 ) ( 20 68 ) ( 21 69 ) ( 22 70 ) ( 23 71 ) ( 24 72 ) ( 25 73 ) ( 26 74 ) ( 27 75 ) ( 28 76 ) ( 29 77 ) ( 30 78 ) ( 31 79 ) ( 32 80 ) ( 33 81 ) ( 34 82 ) ( 35 83 ) ( 36 84 ) ( 37 85 ) ( 38 86 ) ( 39 87 ) ( 40 88 ) ( 41 89 ) ( 42 90 ) ( 43 91 ) ( 44 92 ) ( 45 93 ) ( 46 94 ) ( 47 95 )
--------------------------------------------------------------------------------
Level:			2
Size:			512 kB
Cache groups:		( 0 48 ) ( 1 49 ) ( 2 50 ) ( 3 51 ) ( 4 52 ) ( 5 53 ) ( 6 54 ) ( 7 55 ) ( 8 56 ) ( 9 57 ) ( 10 58 ) ( 11 59 ) ( 12 60 ) ( 13 61 ) ( 14 62 ) ( 15 63 ) ( 16 64 ) ( 17 65 ) ( 18 66 ) ( 19 67 ) ( 20 68 ) ( 21 69 ) ( 22 70 ) ( 23 71 ) ( 24 72 ) ( 25 73 ) ( 26 74 ) ( 27 75 ) ( 28 76 ) ( 29 77 ) ( 30 78 ) ( 31 79 ) ( 32 80 ) ( 33 81 ) ( 34 82 ) ( 35 83 ) ( 36 84 ) ( 37 85 ) ( 38 86 ) ( 39 87 ) ( 40 88 ) ( 41 89 ) ( 42 90 ) ( 43 91 ) ( 44 92 ) ( 45 93 ) ( 46 94 ) ( 47 95 )
--------------------------------------------------------------------------------
Level:			3
Size:			8 MB
Cache groups:		( 0 48 1 49 2 50 ) ( 3 51 4 52 5 53 ) ( 6 54 7 55 8 56 ) ( 9 57 10 58 11 59 ) ( 12 60 13 61 14 62 ) ( 15 63 16 64 17 65 ) ( 18 66 19 67 20 68 ) ( 21 69 22 70 23 71 ) ( 24 72 25 73 26 74 ) ( 27 75 28 76 29 77 ) ( 30 78 31 79 32 80 ) ( 33 81 34 82 35 83 ) ( 36 84 37 85 38 86 ) ( 39 87 40 88 41 89 ) ( 42 90 43 91 44 92 ) ( 45 93 46 94 47 95 )
--------------------------------------------------------------------------------
********************************************************************************
NUMA Topology
********************************************************************************
NUMA domains:		8
--------------------------------------------------------------------------------
Domain:			0
Processors:		( 0 48 1 49 2 50 3 51 4 52 5 53 )
Distances:		10 16 16 16 32 32 32 32
Free memory:		15828.4 MB
Total memory:		15967 MB
--------------------------------------------------------------------------------
Domain:			1
Processors:		( 6 54 7 55 8 56 9 57 10 58 11 59 )
Distances:		16 10 16 16 32 32 32 32
Free memory:		15979.6 MB
Total memory:		16124.4 MB
--------------------------------------------------------------------------------
Domain:			2
Processors:		( 12 60 13 61 14 62 15 63 16 64 17 65 )
Distances:		16 16 10 16 32 32 32 32
Free memory:		16002.8 MB
Total memory:		16124.5 MB
--------------------------------------------------------------------------------
Domain:			3
Processors:		( 18 66 19 67 20 68 21 69 22 70 23 71 )
Distances:		16 16 16 10 32 32 32 32
Free memory:		15959.5 MB
Total memory:		16103.3 MB
--------------------------------------------------------------------------------
Domain:			4
Processors:		( 24 72 25 73 26 74 27 75 28 76 29 77 )
Distances:		32 32 32 32 10 16 16 16
Free memory:		15771.6 MB
Total memory:		16124.5 MB
--------------------------------------------------------------------------------
Domain:			5
Processors:		( 30 78 31 79 32 80 33 81 34 82 35 83 )
Distances:		32 32 32 32 16 10 16 16
Free memory:		15739 MB
Total memory:		16124.4 MB
--------------------------------------------------------------------------------
Domain:			6
Processors:		( 36 84 37 85 38 86 39 87 40 88 41 89 )
Distances:		32 32 32 32 16 16 10 16
Free memory:		15833.7 MB
Total memory:		16124.5 MB
--------------------------------------------------------------------------------
Domain:			7
Processors:		( 42 90 43 91 44 92 45 93 46 94 47 95 )
Distances:		32 32 32 32 16 16 16 10
Free memory:		15532.5 MB
Total memory:		16122.9 MB
--------------------------------------------------------------------------------

################################################################################
# NUMA Topology
################################################################################
available: 8 nodes (0-7)
node 0 cpus: 0 1 2 3 4 5 48 49 50 51 52 53
node 0 size: 15966 MB
node 0 free: 15828 MB
node 1 cpus: 6 7 8 9 10 11 54 55 56 57 58 59
node 1 size: 16124 MB
node 1 free: 15979 MB
node 2 cpus: 12 13 14 15 16 17 60 61 62 63 64 65
node 2 size: 16124 MB
node 2 free: 16002 MB
node 3 cpus: 18 19 20 21 22 23 66 67 68 69 70 71
node 3 size: 16103 MB
node 3 free: 15959 MB
node 4 cpus: 24 25 26 27 28 29 72 73 74 75 76 77
node 4 size: 16124 MB
node 4 free: 15771 MB
node 5 cpus: 30 31 32 33 34 35 78 79 80 81 82 83
node 5 size: 16124 MB
node 5 free: 15749 MB
node 6 cpus: 36 37 38 39 40 41 84 85 86 87 88 89
node 6 size: 16124 MB
node 6 free: 15834 MB
node 7 cpus: 42 43 44 45 46 47 90 91 92 93 94 95
node 7 size: 16122 MB
node 7 free: 15532 MB
node distances:
node   0   1   2   3   4   5   6   7
  0:  10  16  16  16  32  32  32  32
  1:  16  10  16  16  32  32  32  32
  2:  16  16  10  16  32  32  32  32
  3:  16  16  16  10  32  32  32  32
  4:  32  32  32  32  10  16  16  16
  5:  32  32  32  32  16  10  16  16
  6:  32  32  32  32  16  16  10  16
  7:  32  32  32  32  16  16  16  10

################################################################################
# Frequencies
################################################################################
Current CPU frequencies:
CPU 0: governor  performance min/cur/max 2.3/2.164/2.3 GHz Turbo 0
CPU 1: governor  performance min/cur/max 2.3/1.847/2.3 GHz Turbo 0
CPU 2: governor  performance min/cur/max 2.3/1.846/2.3 GHz Turbo 0
CPU 3: governor  performance min/cur/max 2.3/1.847/2.3 GHz Turbo 0
CPU 4: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 5: governor  performance min/cur/max 2.3/1.847/2.3 GHz Turbo 0
CPU 6: governor  performance min/cur/max 2.3/1.851/2.3 GHz Turbo 0
CPU 7: governor  performance min/cur/max 2.3/2.181/2.3 GHz Turbo 0
CPU 8: governor  performance min/cur/max 2.3/1.845/2.3 GHz Turbo 0
CPU 9: governor  performance min/cur/max 2.3/1.851/2.3 GHz Turbo 0
CPU 10: governor  performance min/cur/max 2.3/1.848/2.3 GHz Turbo 0
CPU 11: governor  performance min/cur/max 2.3/1.836/2.3 GHz Turbo 0
CPU 12: governor  performance min/cur/max 2.3/1.848/2.3 GHz Turbo 0
CPU 13: governor  performance min/cur/max 2.3/1.848/2.3 GHz Turbo 0
CPU 14: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 15: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 16: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 17: governor  performance min/cur/max 2.3/1.853/2.3 GHz Turbo 0
CPU 18: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 19: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 20: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 21: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 22: governor  performance min/cur/max 2.3/1.851/2.3 GHz Turbo 0
CPU 23: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 24: governor  performance min/cur/max 2.3/2.239/2.3 GHz Turbo 0
CPU 25: governor  performance min/cur/max 2.3/2.165/2.3 GHz Turbo 0
CPU 26: governor  performance min/cur/max 2.3/2.253/2.3 GHz Turbo 0
CPU 27: governor  performance min/cur/max 2.3/2.106/2.3 GHz Turbo 0
CPU 28: governor  performance min/cur/max 2.3/2.033/2.3 GHz Turbo 0
CPU 29: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 30: governor  performance min/cur/max 2.3/2.088/2.3 GHz Turbo 0
CPU 31: governor  performance min/cur/max 2.3/2.103/2.3 GHz Turbo 0
CPU 32: governor  performance min/cur/max 2.3/2.078/2.3 GHz Turbo 0
CPU 33: governor  performance min/cur/max 2.3/2.197/2.3 GHz Turbo 0
CPU 34: governor  performance min/cur/max 2.3/2.273/2.3 GHz Turbo 0
CPU 35: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 36: governor  performance min/cur/max 2.3/2.264/2.3 GHz Turbo 0
CPU 37: governor  performance min/cur/max 2.3/2.264/2.3 GHz Turbo 0
CPU 38: governor  performance min/cur/max 2.3/2.129/2.3 GHz Turbo 0
CPU 39: governor  performance min/cur/max 2.3/2.094/2.3 GHz Turbo 0
CPU 40: governor  performance min/cur/max 2.3/2.278/2.3 GHz Turbo 0
CPU 41: governor  performance min/cur/max 2.3/1.971/2.3 GHz Turbo 0
CPU 42: governor  performance min/cur/max 2.3/2.264/2.3 GHz Turbo 0
CPU 43: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 44: governor  performance min/cur/max 2.3/2.153/2.3 GHz Turbo 0
CPU 45: governor  performance min/cur/max 2.3/2.260/2.3 GHz Turbo 0
CPU 46: governor  performance min/cur/max 2.3/1.926/2.3 GHz Turbo 0
CPU 47: governor  performance min/cur/max 2.3/2.230/2.3 GHz Turbo 0
CPU 48: governor  performance min/cur/max 2.3/1.852/2.3 GHz Turbo 0
CPU 49: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 50: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 51: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 52: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 53: governor  performance min/cur/max 2.3/1.847/2.3 GHz Turbo 0
CPU 54: governor  performance min/cur/max 2.3/2.023/2.3 GHz Turbo 0
CPU 55: governor  performance min/cur/max 2.3/2.159/2.3 GHz Turbo 0
CPU 56: governor  performance min/cur/max 2.3/1.848/2.3 GHz Turbo 0
CPU 57: governor  performance min/cur/max 2.3/1.848/2.3 GHz Turbo 0
CPU 58: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 59: governor  performance min/cur/max 2.3/1.846/2.3 GHz Turbo 0
CPU 60: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 61: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 62: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 63: governor  performance min/cur/max 2.3/1.847/2.3 GHz Turbo 0
CPU 64: governor  performance min/cur/max 2.3/1.987/2.3 GHz Turbo 0
CPU 65: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 66: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 67: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 68: governor  performance min/cur/max 2.3/1.835/2.3 GHz Turbo 0
CPU 69: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 70: governor  performance min/cur/max 2.3/1.851/2.3 GHz Turbo 0
CPU 71: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 72: governor  performance min/cur/max 2.3/2.090/2.3 GHz Turbo 0
CPU 73: governor  performance min/cur/max 2.3/1.998/2.3 GHz Turbo 0
CPU 74: governor  performance min/cur/max 2.3/2.249/2.3 GHz Turbo 0
CPU 75: governor  performance min/cur/max 2.3/2.142/2.3 GHz Turbo 0
CPU 76: governor  performance min/cur/max 2.3/1.849/2.3 GHz Turbo 0
CPU 77: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 78: governor  performance min/cur/max 2.3/1.944/2.3 GHz Turbo 0
CPU 79: governor  performance min/cur/max 2.3/1.975/2.3 GHz Turbo 0
CPU 80: governor  performance min/cur/max 2.3/1.966/2.3 GHz Turbo 0
CPU 81: governor  performance min/cur/max 2.3/1.846/2.3 GHz Turbo 0
CPU 82: governor  performance min/cur/max 2.3/1.948/2.3 GHz Turbo 0
CPU 83: governor  performance min/cur/max 2.3/2.169/2.3 GHz Turbo 0
CPU 84: governor  performance min/cur/max 2.3/2.131/2.3 GHz Turbo 0
CPU 85: governor  performance min/cur/max 2.3/2.152/2.3 GHz Turbo 0
CPU 86: governor  performance min/cur/max 2.3/2.060/2.3 GHz Turbo 0
CPU 87: governor  performance min/cur/max 2.3/2.264/2.3 GHz Turbo 0
CPU 88: governor  performance min/cur/max 2.3/2.240/2.3 GHz Turbo 0
CPU 89: governor  performance min/cur/max 2.3/2.079/2.3 GHz Turbo 0
CPU 90: governor  performance min/cur/max 2.3/2.088/2.3 GHz Turbo 0
CPU 91: governor  performance min/cur/max 2.3/2.204/2.3 GHz Turbo 0
CPU 92: governor  performance min/cur/max 2.3/2.276/2.3 GHz Turbo 0
CPU 93: governor  performance min/cur/max 2.3/2.207/2.3 GHz Turbo 0
CPU 94: governor  performance min/cur/max 2.3/1.850/2.3 GHz Turbo 0
CPU 95: governor  performance min/cur/max 2.3/2.168/2.3 GHz Turbo 0

No support for Uncore frequencies

################################################################################
# Prefetchers
################################################################################
INFO: Manipulation of CPU features is only available on Intel platforms

################################################################################
# Load
################################################################################
0.14 0.03 0.01 1/1071 48127

################################################################################
# Performance energy bias
################################################################################
Performance energy bias: 0 (0=highest performance, 15 = lowest energy)

################################################################################
# NUMA balancing
################################################################################
Enabled: 0

################################################################################
# General memory info
################################################################################
MemTotal:       131907092 kB
MemFree:        129706028 kB
MemAvailable:   129611272 kB
Buffers:           31980 kB
Cached:           493452 kB
SwapCached:            0 kB
Active:           432036 kB
Inactive:         143152 kB
Active(anon):      50028 kB
Inactive(anon):     1544 kB
Active(file):     382008 kB
Inactive(file):   141608 kB
Unevictable:           0 kB
Mlocked:               0 kB
SwapTotal:      67057660 kB
SwapFree:       67057660 kB
Dirty:               328 kB
Writeback:             0 kB
AnonPages:         49804 kB
Mapped:            63604 kB
Shmem:              1820 kB
Slab:            1074448 kB
SReclaimable:     398824 kB
SUnreclaim:       675624 kB
KernelStack:       19168 kB
PageTables:         3348 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    133011204 kB
Committed_AS:     285612 kB
VmallocTotal:   34359738367 kB
VmallocUsed:           0 kB
VmallocChunk:          0 kB
HardwareCorrupted:     0 kB
AnonHugePages:      6144 kB
ShmemHugePages:        0 kB
ShmemPmdMapped:        0 kB
CmaTotal:              0 kB
CmaFree:               0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:     1238084 kB
DirectMap2M:    72062976 kB
DirectMap1G:    60817408 kB

################################################################################
# Transparent huge pages
################################################################################
Enabled: [always] madvise never
Use zero page: 1

################################################################################
# Hardware power limits
################################################################################

################################################################################
# Compiler
################################################################################
icc (ICC) 19.0.2.187 20190117
Copyright (C) 1985-2019 Intel Corporation.  All rights reserved.


################################################################################
# MPI
################################################################################
Intel(R) MPI Library for Linux* OS, Version 2019 Update 2 Build 20190123 (id: e2d820d49)
Copyright 2003-2019, Intel Corporation.

################################################################################
# dmidecode
################################################################################
# dmidecode 3.1
Getting SMBIOS data from sysfs.
SMBIOS 3.1.1 present.

Handle 0x0000, DMI type 0, 26 bytes
BIOS Information
	Vendor: American Megatrends Inc.
	Version: 1.0c
	Release Date: 12/22/2017
	Address: 0xF0000
	Runtime Size: 64 kB
	ROM Size: 16 MB
	Characteristics:
		PCI is supported
		BIOS is upgradeable
		BIOS shadowing is allowed
		Boot from CD is supported
		Selectable boot is supported
		BIOS ROM is socketed
		EDD is supported
		5.25"/1.2 MB floppy services are supported (int 13h)
		3.5"/720 kB floppy services are supported (int 13h)
		3.5"/2.88 MB floppy services are supported (int 13h)
		Print screen service is supported (int 5h)
	(Line containing Serial number has been censored)
		Printer services are supported (int 17h)
		ACPI is supported
		USB legacy is supported
		BIOS boot specification is supported
		Targeted content distribution is supported
		UEFI is supported
	BIOS Revision: 5.13

Handle 0x0001, DMI type 1, 27 bytes
System Information
	Manufacturer: Supermicro
	Product Name: AS -1023US-TR4
	Version: 0123456789
	(Line containing Serial number has been censored)
	(Line containing UUID has been censored)
	Wake-up Type: Power Switch
	SKU Number: To be filled by O.E.M.
	Family: To be filled by O.E.M.

Handle 0x0002, DMI type 2, 15 bytes
Base Board Information
	Manufacturer: Supermicro
	Product Name: H11DSU-iN
	Version: 1.02A
	(Line containing Serial number has been censored)
	Asset Tag: To be filled by O.E.M.
	Features:
		Board is a hosting board
		Board is removable
		Board is replaceable
	Location In Chassis: To be filled by O.E.M.
	Chassis Handle: 0x0003
	Type: Motherboard
	Contained Object Handles: 0

Handle 0x0003, DMI type 3, 22 bytes
Chassis Information
	Manufacturer: Supermicro
	Type: Other
	Lock: Not Present
	Version: 0123456789
	(Line containing Serial number has been censored)
	Asset Tag: To be filled by O.E.M.
	Boot-up State: Safe
	Power Supply State: Safe
	Thermal State: Safe
	Security Status: None
	OEM Information: 0x00000000
	Height: Unspecified
	Number Of Power Cords: 1
	Contained Elements: 0
	SKU Number: To be filled by O.E.M.

Handle 0x0004, DMI type 8, 9 bytes
Port Connector Information
	Internal Reference Designator: JVGA1
	Internal Connector Type: None
	External Reference Designator: VGA
	External Connector Type: DB-25 female
	Port Type: Video Port

Handle 0x0005, DMI type 8, 9 bytes
Port Connector Information
	Internal Reference Designator: JCOM1
	Internal Connector Type: None
	External Reference Designator: COM1
	External Connector Type: DB-9 male
	(Line containing Serial number has been censored)

Handle 0x0006, DMI type 8, 9 bytes
Port Connector Information
	Internal Reference Designator: JLAN1
	Internal Connector Type: None
	External Reference Designator: IPMI_LAN
	External Connector Type: RJ-45
	Port Type: Network Port

Handle 0x0007, DMI type 8, 9 bytes
Port Connector Information
	Internal Reference Designator: J36
	Internal Connector Type: None
	External Reference Designator: USB0/1(3.0)
	External Connector Type: Access Bus (USB)
	Port Type: USB

Handle 0x0008, DMI type 8, 9 bytes
Port Connector Information
	Internal Reference Designator: JUSBA1
	Internal Connector Type: None
	External Reference Designator: USB2(3.0)
	External Connector Type: Access Bus (USB)
	Port Type: USB

Handle 0x0009, DMI type 8, 9 bytes
Port Connector Information
	Internal Reference Designator: JUSB3
	Internal Connector Type: None
	External Reference Designator: USB3/4(3.0)
	External Connector Type: Access Bus (USB)
	Port Type: USB

Handle 0x000B, DMI type 32, 20 bytes
System Boot Information
	Status: No errors detected

Handle 0x000E, DMI type 41, 11 bytes
Onboard Device
	Reference Designation: ASPEED Video AST2500
	Type: Video
	Status: Enabled
	Type Instance: 1
	Bus Address: 0000:02:00.0

Handle 0x000F, DMI type 41, 11 bytes
Onboard Device
	Reference Designation: ASMedia USB 3.1
	Type: Other
	Status: Enabled
	Type Instance: 1
	Bus Address: 0000:03:00.0

Handle 0x0010, DMI type 41, 11 bytes
Onboard Device
	Reference Designation: ASMedia USB 3.1
	Type: Other
	Status: Enabled
	Type Instance: 2
	Bus Address: 0000:04:00.0

Handle 0x0017, DMI type 15, 73 bytes
System Event Log
	Area Length: 65535 bytes
	Header Start Offset: 0x0000
	Header Length: 16 bytes
	Data Start Offset: 0x0010
	Access Method: Memory-mapped physical 32-bit address
	Access Address: 0xFF2A4000
	Status: Valid, Not Full
	Change Token: 0x00000001
	Header Format: Type 1
	Supported Log Type Descriptors: 25
	Descriptor 1: Single-bit ECC memory error
	Data Format 1: Multiple-event handle
	Descriptor 2: Multi-bit ECC memory error
	Data Format 2: Multiple-event handle
	Descriptor 3: Parity memory error
	Data Format 3: Multiple-event handle
	Descriptor 4: Bus timeout
	Data Format 4: None
	Descriptor 5: I/O channel block
	Data Format 5: None
	Descriptor 6: Software NMI
	Data Format 6: None
	Descriptor 7: POST memory resize
	Data Format 7: None
	Descriptor 8: POST error
	Data Format 8: POST results bitmap
	Descriptor 9: PCI parity error
	Data Format 9: Multiple-event handle
	Descriptor 10: PCI system error
	Data Format 10: Multiple-event handle
	Descriptor 11: CPU failure
	Data Format 11: None
	Descriptor 12: EISA failsafe timer timeout
	Data Format 12: None
	Descriptor 13: Correctable memory log disabled
	Data Format 13: None
	Descriptor 14: Logging disabled
	Data Format 14: None
	Descriptor 15: System limit exceeded
	Data Format 15: None
	Descriptor 16: Asynchronous hardware timer expired
	Data Format 16: None
	Descriptor 17: System configuration information
	Data Format 17: None
	Descriptor 18: Hard disk information
	Data Format 18: None
	Descriptor 19: System reconfigured
	Data Format 19: None
	Descriptor 20: Uncorrectable CPU-complex error
	Data Format 20: None
	Descriptor 21: Log area reset/cleared
	Data Format 21: None
	Descriptor 22: System boot
	Data Format 22: None
	Descriptor 23: End of log
	Data Format 23: None
	Descriptor 24: OEM-specific
	Data Format 24: OEM-specific
	Descriptor 25: OEM-specific
	Data Format 25: OEM-specific

Handle 0x0019, DMI type 16, 23 bytes
Physical Memory Array
	Location: System Board Or Motherboard
	Use: System Memory
	Error Correction Type: Multi-bit ECC
	Maximum Capacity: 2 TB
	Error Information Handle: 0x0018
	Number Of Devices: 32

Handle 0x001C, DMI type 7, 27 bytes
Cache Information
	Socket Designation: L1 Cache
	Configuration: Enabled, Not Socketed, Level 1
	Operational Mode: Write Back
	Location: Internal
	Installed Size: 2304 kB
	Maximum Size: 2304 kB
	Supported SRAM Types:
		Pipeline Burst
	Installed SRAM Type: Pipeline Burst
	Speed: 1 ns
	Error Correction Type: Multi-bit ECC
	System Type: Unified
	Associativity: 8-way Set-associative

Handle 0x001D, DMI type 7, 27 bytes
Cache Information
	Socket Designation: L2 Cache
	Configuration: Enabled, Not Socketed, Level 2
	Operational Mode: Write Back
	Location: Internal
	Installed Size: 12288 kB
	Maximum Size: 12288 kB
	Supported SRAM Types:
		Pipeline Burst
	Installed SRAM Type: Pipeline Burst
	Speed: 1 ns
	Error Correction Type: Multi-bit ECC
	System Type: Unified
	Associativity: 8-way Set-associative

Handle 0x001E, DMI type 7, 27 bytes
Cache Information
	Socket Designation: L3 Cache
	Configuration: Enabled, Not Socketed, Level 3
	Operational Mode: Write Back
	Location: Internal
	Installed Size: 65536 kB
	Maximum Size: 65536 kB
	Supported SRAM Types:
		Pipeline Burst
	Installed SRAM Type: Pipeline Burst
	Speed: 1 ns
	Error Correction Type: Multi-bit ECC
	System Type: Unified
	Associativity: 64-way Set-associative

Handle 0x001F, DMI type 4, 48 bytes
Processor Information
	Socket Designation: CPU1
	Type: Central Processor
	Family: Zen
	Manufacturer: Advanced Micro Devices, Inc.
	ID: 12 0F 80 00 FF FB 8B 17
	Signature: Family 23, Model 1, Stepping 2
	Flags:
		FPU (Floating-point unit on-chip)
		VME (Virtual mode extension)
		DE (Debugging extension)
		PSE (Page size extension)
		TSC (Time stamp counter)
		MSR (Model specific registers)
		PAE (Physical address extension)
		MCE (Machine check exception)
		CX8 (CMPXCHG8 instruction supported)
		APIC (On-chip APIC hardware supported)
		SEP (Fast system call)
		MTRR (Memory type range registers)
		PGE (Page global enable)
		MCA (Machine check architecture)
		CMOV (Conditional move instruction supported)
		PAT (Page attribute table)
		PSE-36 (36-bit page size extension)
		CLFSH (CLFLUSH instruction supported)
		MMX (MMX technology supported)
		FXSR (FXSAVE and FXSTOR instructions supported)
		SSE (Streaming SIMD extensions)
		SSE2 (Streaming SIMD extensions 2)
		HTT (Multi-threading)
	Version: AMD EPYC 7451 24-Core Processor
	Voltage: 1.0 V
	External Clock: 100 MHz
	Max Speed: 3200 MHz
	Current Speed: 2300 MHz
	Status: Populated, Enabled
	Upgrade: Socket SP3
	L1 Cache Handle: 0x001C
	L2 Cache Handle: 0x001D
	L3 Cache Handle: 0x001E
	(Line containing Serial number has been censored)
	Asset Tag: Unknown
	Part Number: Unknown
	Core Count: 24
	Core Enabled: 24
	Thread Count: 48
	Characteristics:
		64-bit capable
		Multi-Core
		Hardware Thread
		Execute Protection
		Enhanced Virtualization
		Power/Performance Control

Handle 0x0020, DMI type 7, 27 bytes
Cache Information
	Socket Designation: L1 Cache
	Configuration: Enabled, Not Socketed, Level 1
	Operational Mode: Write Back
	Location: Internal
	Installed Size: 2304 kB
	Maximum Size: 2304 kB
	Supported SRAM Types:
		Pipeline Burst
	Installed SRAM Type: Pipeline Burst
	Speed: 1 ns
	Error Correction Type: Multi-bit ECC
	System Type: Unified
	Associativity: 8-way Set-associative

Handle 0x0021, DMI type 7, 27 bytes
Cache Information
	Socket Designation: L2 Cache
	Configuration: Enabled, Not Socketed, Level 2
	Operational Mode: Write Back
	Location: Internal
	Installed Size: 12288 kB
	Maximum Size: 12288 kB
	Supported SRAM Types:
		Pipeline Burst
	Installed SRAM Type: Pipeline Burst
	Speed: 1 ns
	Error Correction Type: Multi-bit ECC
	System Type: Unified
	Associativity: 8-way Set-associative

Handle 0x0022, DMI type 7, 27 bytes
Cache Information
	Socket Designation: L3 Cache
	Configuration: Enabled, Not Socketed, Level 3
	Operational Mode: Write Back
	Location: Internal
	Installed Size: 65536 kB
	Maximum Size: 65536 kB
	Supported SRAM Types:
		Pipeline Burst
	Installed SRAM Type: Pipeline Burst
	Speed: 1 ns
	Error Correction Type: Multi-bit ECC
	System Type: Unified
	Associativity: 64-way Set-associative

Handle 0x0023, DMI type 4, 48 bytes
Processor Information
	Socket Designation: CPU2
	Type: Central Processor
	Family: Zen
	Manufacturer: Advanced Micro Devices, Inc.
	ID: 12 0F 80 00 FF FB 8B 17
	Signature: Family 23, Model 1, Stepping 2
	Flags:
		FPU (Floating-point unit on-chip)
		VME (Virtual mode extension)
		DE (Debugging extension)
		PSE (Page size extension)
		TSC (Time stamp counter)
		MSR (Model specific registers)
		PAE (Physical address extension)
		MCE (Machine check exception)
		CX8 (CMPXCHG8 instruction supported)
		APIC (On-chip APIC hardware supported)
		SEP (Fast system call)
		MTRR (Memory type range registers)
		PGE (Page global enable)
		MCA (Machine check architecture)
		CMOV (Conditional move instruction supported)
		PAT (Page attribute table)
		PSE-36 (36-bit page size extension)
		CLFSH (CLFLUSH instruction supported)
		MMX (MMX technology supported)
		FXSR (FXSAVE and FXSTOR instructions supported)
		SSE (Streaming SIMD extensions)
		SSE2 (Streaming SIMD extensions 2)
		HTT (Multi-threading)
	Version: AMD EPYC 7451 24-Core Processor
	Voltage: 1.0 V
	External Clock: 100 MHz
	Max Speed: 3200 MHz
	Current Speed: 2300 MHz
	Status: Populated, Enabled
	Upgrade: Socket SP3
	L1 Cache Handle: 0x0020
	L2 Cache Handle: 0x0021
	L3 Cache Handle: 0x0022
	(Line containing Serial number has been censored)
	Asset Tag: Unknown
	Part Number: Unknown
	Core Count: 24
	Core Enabled: 24
	Thread Count: 48
	Characteristics:
		64-bit capable
		Multi-Core
		Hardware Thread
		Execute Protection
		Enhanced Virtualization
		Power/Performance Control

Handle 0x0025, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0024
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P1-DIMMA1
	Bank Locator: P0_Node0_Channel0_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0027, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0026
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P1-DIMMA2
	Bank Locator: P0_Node0_Channel0_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P1-DIMMA2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x002A, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0029
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P1-DIMMB1
	Bank Locator: P0_Node0_Channel1_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x002C, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x002B
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P1-DIMMB2
	Bank Locator: P0_Node0_Channel1_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P1-DIMMB2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x002F, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x002E
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P1-DIMMC1
	Bank Locator: P0_Node0_Channel2_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0031, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0030
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P1-DIMMC2
	Bank Locator: P0_Node0_Channel2_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P1-DIMMC2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0034, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0033
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P1-DIMMD1
	Bank Locator: P0_Node0_Channel3_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0036, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0035
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P1-DIMMD2
	Bank Locator: P0_Node0_Channel3_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P1-DIMMD2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0039, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0038
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P1-DIMME1
	Bank Locator: P0_Node0_Channel4_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x003B, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x003A
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P1-DIMME2
	Bank Locator: P0_Node0_Channel4_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P1-DIMME2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x003E, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x003D
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P1-DIMMF1
	Bank Locator: P0_Node0_Channel5_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0040, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x003F
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P1-DIMMF2
	Bank Locator: P0_Node0_Channel5_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P1-DIMMF2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0043, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0042
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P1-DIMMG1
	Bank Locator: P0_Node0_Channel6_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0045, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0044
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P1-DIMMG2
	Bank Locator: P0_Node0_Channel6_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P1-DIMMG2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0048, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0047
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P1-DIMMH1
	Bank Locator: P0_Node0_Channel7_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x004A, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0049
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P1-DIMMH2
	Bank Locator: P0_Node0_Channel7_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P1-DIMMH2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x004D, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x004C
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P2-DIMMA1
	Bank Locator: P1_Node0_Channel0_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x004F, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x004E
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P2-DIMMA2
	Bank Locator: P1_Node0_Channel0_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P2-DIMMA2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0052, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0051
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P2-DIMMB1
	Bank Locator: P1_Node0_Channel1_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0054, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0053
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P2-DIMMB2
	Bank Locator: P1_Node0_Channel1_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P2-DIMMB2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0057, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0056
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P2-DIMMC1
	Bank Locator: P1_Node0_Channel2_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0059, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0058
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P2-DIMMC2
	Bank Locator: P1_Node0_Channel2_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P2-DIMMC2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x005C, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x005B
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P2-DIMMD1
	Bank Locator: P1_Node0_Channel3_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x005E, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x005D
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P2-DIMMD2
	Bank Locator: P1_Node0_Channel3_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P2-DIMMD2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0061, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0060
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P2-DIMME1
	Bank Locator: P1_Node0_Channel4_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0063, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0062
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P2-DIMME2
	Bank Locator: P1_Node0_Channel4_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P2-DIMME2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0066, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0065
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P2-DIMMF1
	Bank Locator: P1_Node0_Channel5_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0068, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0067
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P2-DIMMF2
	Bank Locator: P1_Node0_Channel5_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P2-DIMMF2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x006B, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x006A
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P2-DIMMG1
	Bank Locator: P1_Node0_Channel6_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x006D, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x006C
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P2-DIMMG2
	Bank Locator: P1_Node0_Channel6_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P2-DIMMG2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0070, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x006F
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: Unknown
	Set: None
	Locator: P2-DIMMH1
	Bank Locator: P1_Node0_Channel7_Dimm0
	Type: Unknown
	Type Detail: Unknown
	Speed: Unknown
	Manufacturer: NO DIMM
	(Line containing Serial number has been censored)
	Asset Tag: NO DIMM
	Part Number: NO DIMM
	Rank: Unknown
	Configured Clock Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0072, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0019
	Error Information Handle: 0x0071
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: P2-DIMMH2
	Bank Locator: P1_Node0_Channel7_Dimm1
	Type: DDR4
	Type Detail: Synchronous Registered (Buffered)
	Speed: 2667 MT/s
	Manufacturer: Samsung
	(Line containing Serial number has been censored)
	Asset Tag: P2-DIMMH2_AssetTag (date:16/43)
	Part Number: M393A1G40EB2-CTD
	Rank: 1
	Configured Clock Speed: 2667 MT/s
	Minimum Voltage: 1.2 V
	Maximum Voltage: 1.2 V
	Configured Voltage: 1.2 V

Handle 0x0074, DMI type 9, 17 bytes
System Slot Information
	Designation: RSC-R1UW-2E16 SLOT1 PCI-E X16
	Type: x16 PCI Express 3 x16
	Current Usage: Available
	Length: Long
	ID: 1
	Characteristics:
		3.3 V is provided
		PME signal is supported
	Bus Address: 0000:ff:00.0

Handle 0x0075, DMI type 9, 17 bytes
System Slot Information
	Designation: RSC-R1UW-2E16 SLOT2 PCI-E X16
	Type: x16 PCI Express 3 x16
	Current Usage: Available
	Length: Long
	ID: 2
	Characteristics:
		3.3 V is provided
		PME signal is supported
	Bus Address: 0000:ff:00.0

Handle 0x0077, DMI type 9, 17 bytes
System Slot Information
	Designation: RSC-R1UW-E8R SLOT1 PCI-E X8
	Type: x8 PCI Express 3 x8
	Current Usage: Available
	Length: Short
	ID: 1
	Characteristics:
		3.3 V is provided
		PME signal is supported
	Bus Address: 0000:ff:00.0

Handle 0x0079, DMI type 41, 11 bytes
Onboard Device
	Reference Designation: Intel Ethernet I350 #1
	Type: Ethernet
	Status: Enabled
	Type Instance: 1
	Bus Address: 0000:11:00.0

Handle 0x007A, DMI type 41, 11 bytes
Onboard Device
	Reference Designation: Intel Ethernet I350 #2
	Type: Ethernet
	Status: Enabled
	Type Instance: 2
	Bus Address: 0000:11:00.1

Handle 0x007B, DMI type 41, 11 bytes
Onboard Device
	Reference Designation: Intel Ethernet I350 #3
	Type: Ethernet
	Status: Enabled
	Type Instance: 3
	Bus Address: 0000:11:00.2

Handle 0x007C, DMI type 41, 11 bytes
Onboard Device
	Reference Designation: Intel Ethernet I350 #4
	Type: Ethernet
	Status: Enabled
	Type Instance: 4
	Bus Address: 0000:11:00.3

Handle 0x007D, DMI type 9, 17 bytes
System Slot Information
	Designation: AOC-UR-i4G SLOT1 PCI-E 3.0 X8
	Type: x8 PCI Express 3 x8
	Current Usage: Available
	Length: Short
	ID: 1
	Characteristics:
		3.3 V is provided
		PME signal is supported
	Bus Address: 0000:ff:00.0


################################################################################
# environment variables
################################################################################
PBS_ENVIRONMENT=PBS_INTERACTIVE
LD_LIBRARY_PATH=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler/lib/intel64:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler/lib/intel64_lin:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/ipp/lib/intel64:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/lib/intel64/gcc4.7:/apps/intel/ComposerXE2019/debugger_2019/libipt/intel64/lib:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/daal/lib/intel64_lin:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/lib/intel64_lin/gcc4.4:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/libfabric/lib:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/lib/release:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/lib:/apps/gcc/gcc-9.1.0-x86_64/lib64:/apps/gcc/gcc-9.1.0-x86_64/lib:/mnt/opt/likwid-4.3.4/lib
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:
PBS_O_LANG=en_US
MKL_INC=-I/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/include
INCLUDE=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/include
LESSCLOSE=/bin/lesspipe %s %s
MKL_SHLIB=-L/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lpthread -lm
LESS=-R
I_MPI_JOB_RESPECT_PROCESS_PLACEMENT=off
LIKWID_LIBDIR=/mnt/opt/likwid-4.3.4/lib
IPPROOT=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/ipp
LD_RUN_PATH_modshare=/apps/gcc/gcc-9.1.0-x86_64/lib:1:/apps/gcc/gcc-9.1.0-x86_64/lib64:1
OLDPWD=/home/hpc/iwia/iwia84/INSPECT
PBS_O_HOME=/home/hpc/iwia/iwia84
MPICHHOME=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64
RRZECLUSTER=TESTCLUSTER
EDITOR=vi
PBS_JOBID=3373.catstor
PATH_modshare=/usr/bin/vendor_perl:999999999:/home/julian/.local/.bin:999999999:/opt/android-sdk/tools:999999999:/usr/bin:1:/apps/gcc/gcc-9.1.0-x86_64/bin:1:/mnt/opt/likwid-4.3.4/sbin:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/bin:1:/usr/local/bin:999999999:/opt/android-sdk/platform-tools:999999999:/usr/bin/core_perl:999999999:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/bin/intel64:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/rrze-bin-intel:1:/mnt/opt/likwid-4.3.4/bin:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/libfabric/bin:1:/home/julian/.bin:999999999:/bin:1:/apps/python/3.6-anaconda/bin:1:/opt/intel/bin:999999999
MPIHOME=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64
LOADEDMODULES_modshare=intel64/19.0up02:1:intelmpi/2019up02-intel:1:mkl/2019up02:1:gcc/9.1.0:1:python/3.6-anaconda:1:likwid/4.3.4:1:pbspro/default:1
PBS_JOBNAME=STDIN
FPATH=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/include
NCPUS=96
FPATH_modshare=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/include:1
INTEL_F_HOME=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler
CPATH_modshare=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/ipp/include:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/daal/include:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/pstl/include:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/include:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/include:1
WOODYHOME=/home/woody/iwia/iwia84
PBS_O_PATH=/mnt/opt/pbspro/default/bin:/bin:/usr/bin:/usr/local/bin:/opt/android-sdk/platform-tools:/opt/android-sdk/tools:/usr/bin/vendor_perl:/usr/bin/core_perl:/opt/intel/bin:/home/julian/.bin:/home/julian/.local/.bin
LIKWID_FORCE=1
FI_PROVIDER_PATH=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/libfabric/lib/prov
INTEL_PYTHONHOME=/apps/intel/ComposerXE2019/debugger_2019/python/intel64/
MKL_INCDIR=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/include
LD_LIBRARY_PATH_modshare=/apps/gcc/gcc-9.1.0-x86_64/lib:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/lib/intel64/gcc4.7:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/lib:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/lib/release:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/ipp/lib/intel64:1:/mnt/opt/likwid-4.3.4/lib:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler/lib/intel64:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/libfabric/lib:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/daal/lib/intel64_lin:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler/lib/intel64_lin:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin:1:/apps/gcc/gcc-9.1.0-x86_64/lib64:1:/apps/intel/ComposerXE2019/debugger_2019/libipt/intel64/lib:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/lib/intel64_lin/gcc4.4:1
CLASSPATH=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/daal/lib/daal.jar:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/lib/mpi.jar
LESS_TERMCAP_so=[1;44;1m
PBS_CONF_FILE=/etc/pbspro.conf
LESS_TERMCAP_se=[0m
LIBRARY_PATH_modshare=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/ipp/lib/intel64:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler/lib/intel64_lin:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/lib/intel64/gcc4.7:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/daal/lib/intel64_lin:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/lib/intel64_lin/gcc4.4:1
PBS_O_WORKDIR=/home/hpc/iwia/iwia84/INSPECT-repo
USER=iwia84
MPIINCDIR=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/include
I_MPI_HARD_FINALIZE=1
NLSPATH_modshare=/apps/intel/ComposerXE2019/debugger_2019/gdb/intel64/share/locale/%l_%t/%N:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/locale/%l_%t/%N:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler/lib/intel64/locale/%l_%t/%N:1
PBS_NODEFILE=/var/spool/pbspro/aux/3373.catstor
GROUP=iwia
PBS_TASKNUM=1
LIKWID_DEFINES=-DLIKWID_PERFMON
PWD=/home/hpc/iwia/iwia84/INSPECT-repo/stencils/3D_r1_homogeneous_star_constant/Zen_EPYC-7451_20190522_101718
HOME=/home/hpc/iwia/iwia84
LIKWID_LIB=-L/mnt/opt/likwid-4.3.4/lib
CLASSPATH_modshare=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/daal/lib/daal.jar:1:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/lib/mpi.jar:1
CPATH=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/ipp/include:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/pstl/include:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/include:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/daal/include:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/include
PBS_MOMPORT=15003
LIKWID_INCDIR=/mnt/opt/likwid-4.3.4/include
_LMFILES__modshare=/apps/modules/modulefiles/libraries/mkl/2019up02:2:/apps/modules/modulefiles/tools/python/3.6-anaconda:1:/opt/modules/modulefiles/testcluster/likwid/4.3.4:1:/opt/modules/modulefiles/testcluster/pbspro/default:1:/apps/modules/modulefiles/development/intelmpi/2019up02-intel:1:/apps/modules/modulefiles/development/gcc/9.1.0:1
NLSPATH=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler/lib/intel64/locale/%l_%t/%N:/apps/intel/ComposerXE2019/debugger_2019/gdb/intel64/share/locale/%l_%t/%N:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/locale/%l_%t/%N
PBS_JOBCOOKIE=17DB67175832D92452876CAB6952312A
MKL_LIBDIR=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin
PBS_O_SHELL=/bin/bash
MPIINC=-I/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/include
MKL_LIB_THREADED=-Wl,--start-group  /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_intel_lp64.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_intel_thread.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_core.a -Wl,--end-group -lpthread -lm -openmp
LESS_TERMCAP_mb=[1;32m
LESS_TERMCAP_md=[1;34m
LESS_TERMCAP_me=[0m
TMPDIR=/scratch/pbs.3373.catstor
LIBRARY_PATH=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/ipp/lib/intel64:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler/lib/intel64_lin:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/lib/intel64/gcc4.7:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/daal/lib/intel64_lin:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb/lib/intel64_lin/gcc4.4:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin
LIKWID_INC=-I/mnt/opt/likwid-4.3.4/include
LOADEDMODULES=pbspro/default:likwid/4.3.4:python/3.6-anaconda:gcc/9.1.0:intelmpi/2019up02-intel:mkl/2019up02:intel64/19.0up02
DAALROOT=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/daal
MPILIB=-L/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/lib
PBS_CONF=/etc/pbspro.conf
INTEL_LICENSE_FILE=1713@license4
PBS_O_QUEUE=route
MKL_CDFT=-Wl,--start-group  /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_cdft_core.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_intel_lp64.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_intel_thread.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_core.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_blacs_intelmpi_lp64.a -Wl,--end-group -lpthread -lm -openmp
TERM=xterm-256color
SHELL=/bin/bash
MKL_BASE=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl
MANPATH_modshare=:1:/mnt/opt/pbspro/default/man:1:/apps/intel/ComposerXE2019/documentation_2019/en/debugger/gdb-ia/man/:1:/apps/intel/ComposerXE2019/man/common:2:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/man:2:/apps/python/3.6-anaconda/share/man:1:/apps/intel/mpi/man:1:/mnt/opt/likwid-4.3.4/man:1:/apps/gcc/gcc-9.1.0-x86_64/share/man:1
MKL_SLIB_THREADED=-Wl,--start-group -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core -Wl,--end-group -lpthread -lm -openmp
MKLPATH=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin
GDK_USE_XFT=1
TMOUT=3660
LD_RUN_PATH=/apps/gcc/gcc-9.1.0-x86_64/lib64:/apps/gcc/gcc-9.1.0-x86_64/lib
SHLVL=3
PBS_O_HOST=testfront1.rrze.uni-erlangen.de
PYTHONPATH=/home/hpc/iwia/iwia84/kerncraft-osaca/install//lib/python3.6/site-packages/
INTEL_C_HOME=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/compiler
PBS_O_SYSTEM=Linux
MANPATH=/apps/intel/ComposerXE2019/documentation_2019/en/debugger/gdb-ia/man/:/apps/intel/ComposerXE2019/man/common::/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/man:/apps/intel/mpi/man:/apps/gcc/gcc-9.1.0-x86_64/share/man:/apps/python/3.6-anaconda/share/man:/mnt/opt/likwid-4.3.4/man:/mnt/opt/pbspro/default/man
MKL_LIB=-Wl,--start-group /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_intel_lp64.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_sequential.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_core.a -Wl,--end-group -lpthread -lm
PBS_O_LOGNAME=iwia84
PBS_NODENUM=0
MODULEPATH=/opt/modules/modulefiles/testcluster:/apps/modules/modulefiles/applications:/apps/modules/modulefiles/development:/apps/modules/modulefiles/libraries:/apps/modules/modulefiles/tools:/apps/modules/modulefiles/deprecated:/apps/modules/modulefiles/testing
PBS_JOBDIR=/home/hpc/iwia/iwia84
MPIROOTDIR=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64
LOGNAME=iwia84
MKLROOT=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl
MODULEPATH_modshare=/apps/modules/modulefiles/testing:2:/apps/modules/modulefiles/development:2:/apps/modules/modulefiles/applications:2:/opt/modules/modulefiles/testcluster:2:/apps/modules/modulefiles/deprecated:2:/apps/modules/modulefiles/tools:2:/apps/modules/modulefiles/libraries:2
LESS_TERMCAP_ue=[0m
PSTLROOT=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/pstl
LESS_TERMCAP_us=[1;32m
PATH=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/bin/intel64:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/rrze-bin-intel:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/bin:/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi/intel64/libfabric/bin:/apps/gcc/gcc-9.1.0-x86_64/bin:/apps/python/3.6-anaconda/bin:/mnt/opt/likwid-4.3.4/sbin:/mnt/opt/likwid-4.3.4/bin:/bin:/usr/bin:/usr/local/bin:/opt/android-sdk/platform-tools:/opt/android-sdk/tools:/usr/bin/vendor_perl:/usr/bin/core_perl:/opt/intel/bin:/home/julian/.bin:/home/julian/.local/.bin
TBBROOT=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/tbb
_LMFILES_=/opt/modules/modulefiles/testcluster/pbspro/default:/opt/modules/modulefiles/testcluster/likwid/4.3.4:/apps/modules/modulefiles/tools/python/3.6-anaconda:/apps/modules/modulefiles/development/gcc/9.1.0:/apps/modules/modulefiles/development/intelmpi/2019up02-intel:/apps/modules/modulefiles/libraries/mkl/2019up02
PBS_QUEUE=work
MODULESHOME=/apps/modules
INFOPATH_modshare=/apps/intel/ComposerXE2019/documentation_2019/en/debugger/gdb-ia/info/:1
INFOPATH=/apps/intel/ComposerXE2019/documentation_2019/en/debugger/gdb-ia/info/
I_MPI_ROOT=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mpi
QT_XFT=true
INTEL_LICENSE_FILE_modshare=1713@license4:1
MKL_SCALAPACK=/apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_scalapack_lp64.a -Wl,--start-group  /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_intel_lp64.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_intel_thread.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_core.a /apps/intel/ComposerXE2019/compilers_and_libraries_2019.2.187/linux/mkl/lib/intel64_lin/libmkl_blacs_intelmpi_lp64.a -Wl,--end-group -lpthread -lm -openmp
GCC_COLORS=error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01
LESSOPEN=| /bin/lesspipe %s
OMP_NUM_THREADS=96
PBS_O_MAIL=/var/mail/iwia84
_=/usr/bin/env
{%- endcapture -%}

{% include stencil_template.md %}
