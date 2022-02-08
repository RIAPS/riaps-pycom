@0xb487bf324bf367d9;

# RIAPS depl messages

enum Status { ok @0; err @1; }

# Actor registration 
struct ActorRegReq {
  appName @0 : Text;
  version @1 : Text;
  actorName @2 : Text;
  pid @3 : Int32;
  isDevice @4 : Bool;
}

struct ActorRegRep {
  status @0 : Status;
  port @1 : Int32;
  uuid @2 : Text; 
}

struct DeviceArg {
  name @0 : Text;
  value @1 : Text;
}

struct DeviceGetReq {
  appName @0 : Text;
  modelName @1 : Text;
  typeName @2 : Text;
  instName @3 : Text;
  deviceArgs @4 : List(DeviceArg); 
}

struct DeviceGetRep {
  status @0 : Status;
}

struct DeviceRelReq {
  appName @0 : Text;
  modelName @1 : Text;
  typeName @2 : Text;
  instName @3 : Text;
}

struct DeviceRelRep {
  status @0 : Status;
}

struct ActorReportReq {
  appName @0 : Text;
  version @1 : Text;
  actorName @2 : Text;
  msg @3 : Text;
}

struct ActorReportRep {
  status @0 : Status;
}

struct DeplReq {
   union {
      actorReg @0 : ActorRegReq;
      deviceGet @1 : DeviceGetReq;
      deviceRel @2 : DeviceRelReq;
      reportEvent @3 : ActorReportReq;
   }
}

struct DeplRep {
   union {
      actorReg @0 : ActorRegRep;
      deviceGet @1 : DeviceGetRep;
      deviceRel @2 : DeviceRelRep;
      reportEvent @3 : ActorReportRep;
   }
}

struct ResCPUX {
	msg @0 : Text;
}

struct ResMemX {
	msg @0 : Text;
}

struct ResSpcX {
	msg @0 : Text;
}

struct ResNetX {
	msg @0 : Text;
}

struct ResMsg {
	union {
		resCPUX @0 : ResCPUX;
		resMemX @1 : ResMemX;
		resSpcX @2 : ResSpcX;
		resNetX @3 : ResNetX;
	}
}

struct ReinstateMsg {
	msg @0 : Text;
}

enum NICState { up @0; down @1; }

struct NICStateMsg {
	nicState @0: NICState;	
}

enum PeerState { on @0; off @1; }

struct PeerInfoMsg {
	peerState @0 : PeerState;
	uuid @1 : Text; 
}

struct DeplCmd {
	union {
		resourceMsg @0 : ResMsg;
		reinstateCmd @1 : ReinstateMsg;
		nicStateMsg @2 : NICStateMsg;
		peerInfoMsg @3 : PeerInfoMsg;
	}
}
