const states = [
  { name: "PENDING", events: ["PENDINGBIOMETRICALVERIFICATION", "NOVERIFICATIONNEEDED", "PAYMENTFAILED", "ORDERCANCELLED"] },
  { name: "ONHOLD", events: ["BIOMETRICALVERIFICATIONSUCCESSFUL", "VERIFICATIONFAILED", "ORDERCANCELLEDBYUSER"] },
  { name: "PENDINGPAYMENT", events: ["PAYMENTSUCCESSFUL"] },
  { name: "CONFIRMED", events: ["PREPARINGSHIPMENT"] },
  { name: "PROCESSING", events: ["ITEMDISPATCHED"] },
  { name: "SHIPPED", events: ["ITEMRECEIVEDBYCUSTOMER", "DELIVERYISSUE"] },
  { name: "DELIVERED", events: [] },
  { name: "CANCELLED", events: [] },
]

export const stateService = {
  getState(name: string) {
    return states.find(state => state.name === name) ?? { name: "", events: [] };
  }
}